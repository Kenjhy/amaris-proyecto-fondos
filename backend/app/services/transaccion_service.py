import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from uuid import uuid4
from decimal import Decimal
from app.models.transaccion import Transaccion, TransaccionCreate, Subscription
from app.services.cliente_service import ClienteService
from app.services.fondo_service import FondoService
from app.services.notificacion_service import NotificacionService
from app.config import settings

# conexión a DynamoDB nube
dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_REGION)
transaction_table = dynamodb.Table(settings.TRANSACTIONS_TABLE_NAME)
subscription_table = dynamodb.Table(settings.SUBSCRIPTIONS_TABLE_NAME)

#  conexión a DynamoDB local
# dynamodb = boto3.resource(
#     'dynamodb', 
#     endpoint_url='http://localhost:8000',  # Usar DynamoDB local
#     region_name=settings.AWS_REGION,
#     aws_access_key_id='dummy',  # Credenciales dummy para DynamoDB local
#     aws_secret_access_key='dummy'
# )
# transaction_table = dynamodb.Table('Transactions')
# subscription_table = dynamodb.Table('Subscriptions')


# Función auxiliar para convertir tipos para DynamoDB
def convert_types_for_dynamodb(obj):
    if isinstance(obj, dict):
        return {k: convert_types_for_dynamodb(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_types_for_dynamodb(i) for i in obj]
    elif isinstance(obj, float):
        return Decimal(str(obj))
    elif isinstance(obj, datetime):
        return obj.isoformat()  # Convertir datetime a string ISO8601
    return obj

class TransaccionService:
    @staticmethod
    async def create_subscription(client_id: str, subscription_data: TransaccionCreate):
        """Suscribe a un cliente a un fondo"""
        # Obtener información del cliente y del fondo
        client = await ClienteService.get_client(client_id)
        fund = await FondoService.get_fund(subscription_data.fundId)
        
        if not client or not fund:
            return {"error": "Cliente o fondo no encontrado"}
        
        # Verificar saldo suficiente
        if client['balance'] < fund['minimumAmount']:
            return {
                "error": f"No tiene saldo disponible para vincularse al fondo {fund['name']}",
                "status": "FAILED"
            }
        
        # Verificar si ya está suscrito
        try:
            existing = subscription_table.get_item(
                Key={'clientId': client_id, 'fundId': subscription_data.fundId}
            ).get('Item')
            
            if existing and existing['status'] == 'ACTIVE':
                return {"error": "Ya está suscrito a este fondo", "status": "FAILED"}
        except ClientError:
            pass  # Si hay error es porque no existe, lo cual es correcto
        
        # Crear la suscripción
        subscription_id = str(uuid4())
        current_time = datetime.now()
        subscription = Subscription(
            subscriptionId=subscription_id,
            clientId=client_id,
            fundId=subscription_data.fundId,
            amountSubscribed=fund['minimumAmount'],
            status="ACTIVE",
            subscriptionDate=current_time
        )
        
        # Registrar transacción
        transaction_id = str(uuid4())
        transaction = Transaccion(
            transactionId=transaction_id,
            clientId=client_id,
            fundId=subscription_data.fundId,
            type="SUBSCRIPTION",
            amount=fund['minimumAmount'],
            transactionDate=current_time,
            status="COMPLETED"
        )
        
        # Actualizar balance del cliente
        await ClienteService.update_client_balance(client_id, -fund['minimumAmount'])
        
        # Convertir tipos para DynamoDB
        subscription_dict = convert_types_for_dynamodb(subscription.dict())
        transaction_dict = convert_types_for_dynamodb(transaction.dict())
        
        # Guardar transacción y suscripción
        try:
            subscription_table.put_item(Item=subscription_dict)
            transaction_table.put_item(Item=transaction_dict)
            
            # Enviar notificación
            await NotificacionService.send_notification(
                client_id=client_id,
                notification_type=client['preferredNotification'],
                message=f"Se ha suscrito exitosamente al fondo {fund['name']}",
                email=client.get('email'),
                phone=client.get('phone')
            )
            
            return {**transaction.dict(), "fundName": fund['name']}
        except ClientError as e:
            print(f"Error creating subscription: {str(e)}")
            return {"error": "Error al crear suscripción", "status": "FAILED"}

    @staticmethod
    async def cancel_subscription(client_id: str, fund_id: str):
        """Cancela la suscripción de un cliente a un fondo"""
        # Verificar si está suscrito
        try:
            subscription = subscription_table.get_item(
                Key={'clientId': client_id, 'fundId': fund_id}
            ).get('Item')
            
            if not subscription or subscription['status'] != 'ACTIVE':
                return {"error": "No está suscrito a este fondo", "status": "FAILED"}
        except ClientError as e:
            return {"error": f"Error al verificar suscripción: {str(e)}", "status": "FAILED"}
        
        # Obtener información del fondo
        fund = await FondoService.get_fund(fund_id)
        client = await ClienteService.get_client(client_id)
        
        if not fund or not client:
            return {"error": "Fondo o cliente no encontrado", "status": "FAILED"}
        
        # Actualizar la suscripción
        try:
            subscription_table.update_item(
                Key={'clientId': client_id, 'fundId': fund_id},
                UpdateExpression="SET #status = :status",
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={':status': 'CANCELLED'}
            )
        except ClientError as e:
            return {"error": f"Error al cancelar suscripción: {str(e)}", "status": "FAILED"}
        
        # Registrar transacción de cancelación
        transaction_id = str(uuid4())
        current_time = datetime.now()
        transaction = Transaccion(
            transactionId=transaction_id,
            clientId=client_id,
            fundId=fund_id,
            type="CANCELLATION",
            amount=subscription['amountSubscribed'],
            transactionDate=current_time,
            status="COMPLETED"
        )
        
        # Devolver el dinero al cliente
        await ClienteService.update_client_balance(client_id, subscription['amountSubscribed'])
        
        # Convertir tipos para DynamoDB
        transaction_dict = convert_types_for_dynamodb(transaction.dict())
        
        # Guardar transacción
        try:
            transaction_table.put_item(Item=transaction_dict)
            
            # Enviar notificación
            await NotificacionService.send_notification(
                client_id=client_id,
                notification_type=client['preferredNotification'],
                message=f"Ha cancelado exitosamente su suscripción al fondo {fund['name']}",
                email=client.get('email'),
                phone=client.get('phone')
            )
            
            return {**transaction.dict(), "fundName": fund['name']}
        except ClientError as e:
            print(f"Error registering cancellation: {str(e)}")
            return {"error": "Error al registrar cancelación", "status": "FAILED"}

    @staticmethod
    async def get_client_transactions(client_id: str, limit: int = 10):
        """Obtiene el historial de transacciones de un cliente"""
        try:
            response = transaction_table.query(
                KeyConditionExpression="clientId = :cid",
                ExpressionAttributeValues={':cid': client_id},
                ScanIndexForward=False,  # Orden descendente por fecha
                Limit=limit
            )
            
            # Añadir nombres de fondos
            transactions = response.get('Items', [])
            for tx in transactions:
                fund = await FondoService.get_fund(tx['fundId'])
                if fund:
                    tx['fundName'] = fund['name']
            
            return transactions
        except ClientError as e:
            print(f"Error getting transactions: {str(e)}")
            return []

    @staticmethod
    async def get_client_active_subscriptions(client_id: str):
        """Obtiene las suscripciones activas de un cliente"""
        try:
            response = subscription_table.query(
                KeyConditionExpression="clientId = :cid",
                FilterExpression="#status = :status",
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={
                    ':cid': client_id,
                    ':status': 'ACTIVE'
                }
            )
            
            # Añadir nombres de fondos
            subscriptions = response.get('Items', [])
            for sub in subscriptions:
                fund = await FondoService.get_fund(sub['fundId'])
                if fund:
                    sub['fundName'] = fund['name']
            
            return subscriptions
        except ClientError as e:
            print(f"Error getting subscriptions: {str(e)}")
            return []