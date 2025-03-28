import boto3
from decimal import Decimal
import time

# Usar endpoint local para desarrollo
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
client = boto3.client('dynamodb', endpoint_url='http://localhost:8000')

# Lista de nombres de tablas que queremos crear
table_names = ['Clients', 'Funds', 'Subscriptions', 'Transactions']

# Eliminar tablas existentes si existen
existing_tables = client.list_tables()['TableNames']
for table_name in table_names:
    if table_name in existing_tables:
        print(f"Eliminando tabla existente: {table_name}")
        table = dynamodb.Table(table_name)
        table.delete()
        # Esperar a que la tabla se elimine
        print(f"Esperando a que {table_name} se elimine...")
        waiter = client.get_waiter('table_not_exists')
        waiter.wait(TableName=table_name)
        print(f"Tabla {table_name} eliminada.")

# Crear tabla Clients
print("Creando tabla Clients...")
clients_table = dynamodb.create_table(
    TableName='Clients',
    KeySchema=[
        {'AttributeName': 'clientId', 'KeyType': 'HASH'}
    ],
    AttributeDefinitions=[
        {'AttributeName': 'clientId', 'AttributeType': 'S'}
    ],
    ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
)

# Crear tabla Funds
print("Creando tabla Funds...")
funds_table = dynamodb.create_table(
    TableName='Funds',
    KeySchema=[
        {'AttributeName': 'fundId', 'KeyType': 'HASH'}
    ],
    AttributeDefinitions=[
        {'AttributeName': 'fundId', 'AttributeType': 'S'}
    ],
    ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
)

# Crear tabla Subscriptions
print("Creando tabla Subscriptions...")
subscriptions_table = dynamodb.create_table(
    TableName='Subscriptions',
    KeySchema=[
        {'AttributeName': 'clientId', 'KeyType': 'HASH'},
        {'AttributeName': 'fundId', 'KeyType': 'RANGE'}
    ],
    AttributeDefinitions=[
        {'AttributeName': 'clientId', 'AttributeType': 'S'},
        {'AttributeName': 'fundId', 'AttributeType': 'S'}
    ],
    ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
)

# Crear tabla Transactions
print("Creando tabla Transactions...")
try:
    transactions_table = dynamodb.create_table(
        TableName='Transactions',
        KeySchema=[
            {'AttributeName': 'clientId', 'KeyType': 'HASH'},
            {'AttributeName': 'transactionId', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'clientId', 'AttributeType': 'S'},
            {'AttributeName': 'transactionId', 'AttributeType': 'S'},
            {'AttributeName': 'transactionDate', 'AttributeType': 'S'}
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'TransactionsByDate',
                'KeySchema': [
                    {'AttributeName': 'clientId', 'KeyType': 'HASH'},
                    {'AttributeName': 'transactionDate', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
            }
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
except Exception as e:
    print(f"Error al crear la tabla Transactions: {str(e)}")
    # Si hay un error, puede ser porque la tabla se creó parcialmente
    # Intentemos eliminarla y crearla de nuevo
    if 'Transactions' in client.list_tables()['TableNames']:
        print("Eliminando tabla Transactions para intentar de nuevo...")
        dynamodb.Table('Transactions').delete()
        waiter = client.get_waiter('table_not_exists')
        waiter.wait(TableName='Transactions')
        
        # Crear la tabla nuevamente
        print("Intentando crear la tabla Transactions nuevamente...")
        transactions_table = dynamodb.create_table(
            TableName='Transactions',
            KeySchema=[
                {'AttributeName': 'clientId', 'KeyType': 'HASH'},
                {'AttributeName': 'transactionId', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'clientId', 'AttributeType': 'S'},
                {'AttributeName': 'transactionId', 'AttributeType': 'S'},
                {'AttributeName': 'transactionDate', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'TransactionsByDate',
                    'KeySchema': [
                        {'AttributeName': 'clientId', 'KeyType': 'HASH'},
                        {'AttributeName': 'transactionDate', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                }
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )

# Esperar a que todas las tablas estén creadas antes de insertar datos
print("Esperando a que todas las tablas estén creadas...")
for table_name in table_names:
    waiter = client.get_waiter('table_exists')
    waiter.wait(TableName=table_name)
    print(f"Tabla {table_name} creada y disponible.")

# Poblar la tabla de fondos con los datos iniciales - usando Decimal para valores numéricos
print("Cargando datos en la tabla Funds...")
funds_data = [
    {
        'fundId': '1',
        'name': 'FPV_EL CLIENTE_RECAUDADORA',
        'category': 'FPV',
        'minimumAmount': Decimal('75000')
    },
    {
        'fundId': '2',
        'name': 'FPV_EL CLIENTE_ECOPETROL',
        'category': 'FPV',
        'minimumAmount': Decimal('125000')
    },
    {
        'fundId': '3',
        'name': 'DEUDAPRIVADA',
        'category': 'FIC',
        'minimumAmount': Decimal('50000')
    },
    {
        'fundId': '4',
        'name': 'FDO-ACCIONES',
        'category': 'FIC',
        'minimumAmount': Decimal('250000')
    },
    {
        'fundId': '5',
        'name': 'FPV_EL CLIENTE_DINAMICA',
        'category': 'FPV',
        'minimumAmount': Decimal('100000')
    }
]

# Insertar datos de fondos
funds_table = dynamodb.Table('Funds')
for fund in funds_data:
    funds_table.put_item(Item=fund)

# Crear cliente default - usando Decimal para balance
print("Creando cliente por defecto...")
clients_table = dynamodb.Table('Clients')
clients_table.put_item(
    Item={
        'clientId': 'C123456',
        'balance': Decimal('500000'),
        'preferredNotification': 'email',
        'email': 'cliente@ejemplo.com',
        'phone': '+573001234567'
    }
)

print("Tablas creadas y datos iniciales cargados correctamente")