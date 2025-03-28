import boto3
from botocore.exceptions import ClientError
from decimal import Decimal
from app.models.fondo import Fondo
from app.config import settings

# conexión a DynamoDB nube
dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_REGION)
table = dynamodb.Table(settings.FUNDS_TABLE_NAME)


# conexión a DynamoDB local
# dynamodb = boto3.resource(
#     'dynamodb', 
#     endpoint_url='http://localhost:8000',  # Usar DynamoDB local
#     region_name=settings.AWS_REGION,
#     aws_access_key_id='dummy',  # Credenciales dummy para DynamoDB local
#     aws_secret_access_key='dummy'
# )
# table = dynamodb.Table('Funds')


class FondoService:
    @staticmethod
    async def get_all_funds():
        """Obtiene todos los fondos disponibles"""
        try:
            response = table.scan()
            return response.get('Items', [])
        except ClientError as e:
            print(f"Error getting funds: {e.response['Error']['Message']}")
            return []

    @staticmethod
    async def get_fund(fund_id: str):
        """Obtiene un fondo específico por ID"""
        try:
            response = table.get_item(Key={'fundId': fund_id})
            return response.get('Item')
        except ClientError as e:
            print(f"Error getting fund: {e.response['Error']['Message']}")
            return None