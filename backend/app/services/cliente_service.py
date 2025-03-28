import boto3
from botocore.exceptions import ClientError
from decimal import Decimal
from app.models.cliente import Cliente, ClienteUpdate
from app.config import settings

# conexión a DynamoDB nube
dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_REGION)
table = dynamodb.Table(settings.CLIENTS_TABLE_NAME)

# conexión a DynamoDB local
# dynamodb = boto3.resource(
#     'dynamodb', 
#     endpoint_url='http://localhost:8000',  # Usar DynamoDB local
#     region_name=settings.AWS_REGION,
#     aws_access_key_id='dummy',  # Credenciales dummy para DynamoDB local
#     aws_secret_access_key='dummy'
# )
# table = dynamodb.Table('Clients')


# Función auxiliar para convertir floats a Decimal
def float_to_decimal(obj):
    if isinstance(obj, dict):
        return {k: float_to_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [float_to_decimal(i) for i in obj]
    elif isinstance(obj, float):
        return Decimal(str(obj))
    return obj


class ClienteService:
    @staticmethod
    async def get_client(client_id: str):
        try:
            response = table.get_item(Key={'clientId': client_id})
            return response.get('Item')
        except ClientError as e:
            print(f"Error getting client: {e.response['Error']['Message']}")
            return None

    @staticmethod
    async def update_client_balance(client_id: str, amount: float):
        """Actualiza el saldo del cliente (suma o resta)"""
        try:
            # Convertir amount a Decimal
            decimal_amount = Decimal(str(amount))
            
            response = table.update_item(
                Key={'clientId': client_id},
                UpdateExpression="SET balance = balance + :val",
                ExpressionAttributeValues={':val': decimal_amount},
                ReturnValues="UPDATED_NEW"
            )
            return response.get('Attributes')
        except ClientError as e:
            print(f"Error updating balance: {e.response['Error']['Message']}")
            return None

    @staticmethod
    async def update_client_preferences(client_id: str, update_data: ClienteUpdate):
        update_expression = "SET "
        expression_attribute_values = {}
        
        if update_data.preferredNotification:
            update_expression += "preferredNotification = :notification, "
            expression_attribute_values[':notification'] = update_data.preferredNotification
        
        if update_data.email:
            update_expression += "email = :email, "
            expression_attribute_values[':email'] = update_data.email
            
        if update_data.phone:
            update_expression += "phone = :phone, "
            expression_attribute_values[':phone'] = update_data.phone
        
        # Eliminar la última coma
        update_expression = update_expression[:-2]
        
        try:
            response = table.update_item(
                Key={'clientId': client_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="UPDATED_NEW"
            )
            return response.get('Attributes')
        except ClientError as e:
            print(f"Error updating client: {e.response['Error']['Message']}")
            return None