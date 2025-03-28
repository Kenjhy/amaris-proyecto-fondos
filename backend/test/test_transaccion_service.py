import pytest
import boto3
import uuid
from decimal import Decimal
from datetime import datetime
from unittest.mock import patch, MagicMock, ANY, AsyncMock  
from app.models.transaccion import TransaccionCreate, Transaccion, Subscription
from app.services.transaccion_service import TransaccionService, convert_types_for_dynamodb

# Fixtures
@pytest.fixture
def mock_transaction_table():
    with patch('app.services.transaccion_service.transaction_table') as mock_table:
        yield mock_table

@pytest.fixture
def mock_subscription_table():
    with patch('app.services.transaccion_service.subscription_table') as mock_table:
        yield mock_table

@pytest.fixture
def mock_cliente_service():
    with patch('app.services.transaccion_service.ClienteService') as mock_service:
        # Configure get_client to return a coroutine that resolves to the desired value
        mock_service.get_client = AsyncMock()
        yield mock_service
        

@pytest.fixture
def mock_fondo_service():
    with patch('app.services.transaccion_service.FondoService') as mock_service:
        # Configure get_fund to return a coroutine that resolves to the desired value
        mock_service.get_fund = AsyncMock()
        yield mock_service

@pytest.fixture
def mock_notificacion_service():
    with patch('app.services.transaccion_service.NotificacionService') as mock_service:
        yield mock_service

@pytest.fixture
def sample_client_data():
    return {
        'clientId': 'C123456',
        'balance': Decimal('500000'),
        'preferredNotification': 'email',
        'email': 'cliente@ejemplo.com',
        'phone': '+573001234567'
    }

@pytest.fixture
def sample_fund_data():
    return {
        'fundId': '1',
        'name': 'FPV_EL CLIENTE_RECAUDADORA',
        'category': 'FPV',
        'minimumAmount': Decimal('75000')
    }

class TestTransaccionService:
    
    @pytest.mark.asyncio
    async def test_create_subscription_success(
        self, mock_transaction_table, mock_subscription_table,
        mock_cliente_service, mock_fondo_service, mock_notificacion_service,
        sample_client_data, sample_fund_data
    ):
        # Setup
        client_id = 'C123456'
        subscription_data = TransaccionCreate(fundId='1')
        
        # Direct patching of the static methods
        with patch('app.services.transaccion_service.ClienteService.get_client', 
                new_callable=AsyncMock, return_value=sample_client_data):
            with patch('app.services.transaccion_service.FondoService.get_fund', 
                    new_callable=AsyncMock, return_value=sample_fund_data):
                with patch('app.services.transaccion_service.ClienteService.update_client_balance', 
                        new_callable=AsyncMock, return_value={'balance': Decimal('425000')}):
                    with patch('app.services.transaccion_service.NotificacionService.send_notification', 
                            new_callable=AsyncMock, return_value=True):
                        
                        # Mock subscription check (not already subscribed)
                        mock_subscription_table.get_item.return_value = {}
                        
                        # Mock UUID generation for consistent testing
                        with patch('uuid.uuid4', return_value=uuid.UUID('00000000-0000-0000-0000-000000000001')):
                            with patch('app.services.transaccion_service.datetime') as mock_datetime:
                                mock_datetime.now.return_value = datetime(2025, 3, 28, 12, 0, 0)
                                
                                # Execute
                                result = await TransaccionService.create_subscription(client_id, subscription_data)
                                
                                # Assert
                                assert result['fundName'] == 'FPV_EL CLIENTE_RECAUDADORA'
                                assert result['type'] == 'SUBSCRIPTION'
                                assert result['status'] == 'COMPLETED'
                            
                                
    @pytest.mark.asyncio
    async def test_create_subscription_insufficient_balance(
        self, mock_cliente_service, mock_fondo_service,
        sample_fund_data
    ):
        # Setup
        client_id = 'C123456'
        subscription_data = TransaccionCreate(fundId='1')
        
        # Client with insufficient balance
        insufficient_balance_client = {
            'clientId': 'C123456',
            'balance': Decimal('50000'),  # Less than minimum amount for fund
            'preferredNotification': 'email',
            'email': 'cliente@ejemplo.com'
        }
        
        mock_cliente_service.get_client.return_value = insufficient_balance_client
        mock_fondo_service.get_fund.return_value = sample_fund_data
        
        # Execute
        result = await TransaccionService.create_subscription(client_id, subscription_data)
        
        # Assert
        assert 'error' in result
        assert result['status'] == 'FAILED'
        assert 'No tiene saldo disponible' in result['error']
    
    @pytest.mark.asyncio
    async def test_create_subscription_already_subscribed(
        self, mock_subscription_table, mock_cliente_service, mock_fondo_service,
        sample_client_data, sample_fund_data
    ):
        # Setup
        client_id = 'C123456'
        subscription_data = TransaccionCreate(fundId='1')
        
        mock_cliente_service.get_client.return_value = sample_client_data
        mock_fondo_service.get_fund.return_value = sample_fund_data
        
        # Mock existing active subscription
        mock_subscription_table.get_item.return_value = {
            'Item': {
                'clientId': 'C123456',
                'fundId': '1',
                'status': 'ACTIVE'
            }
        }
        
        # Execute
        result = await TransaccionService.create_subscription(client_id, subscription_data)
        
        # Assert
        assert 'error' in result
        assert result['status'] == 'FAILED'
        assert 'Ya está suscrito a este fondo' in result['error']
    
    @pytest.mark.asyncio
    async def test_cancel_subscription_success(
        self, mock_transaction_table, mock_subscription_table,
        mock_cliente_service, mock_fondo_service, mock_notificacion_service,
        sample_client_data, sample_fund_data
    ):
        # Setup
        client_id = 'C123456'
        fund_id = '1'
        
        # Mock active subscription
        mock_subscription_table.get_item.return_value = {
            'Item': {
                'clientId': 'C123456',
                'fundId': '1',
                'status': 'ACTIVE',
                'amountSubscribed': Decimal('75000')
            }
        }
        
        # Direct patching of the static methods
        with patch('app.services.transaccion_service.ClienteService.get_client', 
                new_callable=AsyncMock, return_value=sample_client_data):
            with patch('app.services.transaccion_service.FondoService.get_fund', 
                    new_callable=AsyncMock, return_value=sample_fund_data):
                with patch('app.services.transaccion_service.ClienteService.update_client_balance', 
                        new_callable=AsyncMock, return_value={'balance': Decimal('575000')}):
                    with patch('app.services.transaccion_service.NotificacionService.send_notification', 
                            new_callable=AsyncMock, return_value=True):
                        
                        # Mock UUID generation for consistent testing
                        with patch('uuid.uuid4', return_value=uuid.UUID('00000000-0000-0000-0000-000000000002')):
                            with patch('app.services.transaccion_service.datetime') as mock_datetime:
                                mock_datetime.now.return_value = datetime(2025, 3, 28, 12, 0, 0)
                                
                                # Execute
                                result = await TransaccionService.cancel_subscription(client_id, fund_id)
                                
                                # Assert
                                assert result['fundName'] == 'FPV_EL CLIENTE_RECAUDADORA'
                                assert result['type'] == 'CANCELLATION'
                                assert result['status'] == 'COMPLETED'
                            
    
    @pytest.mark.asyncio
    async def test_cancel_subscription_not_subscribed(self, mock_subscription_table):
        # Setup
        client_id = 'C123456'
        fund_id = '1'
        
        # Mock no active subscription
        mock_subscription_table.get_item.return_value = {}
        
        # Execute
        result = await TransaccionService.cancel_subscription(client_id, fund_id)
        
        # Assert
        assert 'error' in result
        assert result['status'] == 'FAILED'
        assert 'No está suscrito a este fondo' in result['error']
    
    @pytest.mark.asyncio
    async def test_get_client_transactions_success(
        self, mock_transaction_table, mock_fondo_service
    ):
        # Setup
        client_id = 'C123456'
        transactions = [
            {
                'transactionId': '1',
                'clientId': 'C123456',
                'fundId': '1',
                'type': 'SUBSCRIPTION',
                'amount': Decimal('75000'),
                'status': 'COMPLETED'
            },
            {
                'transactionId': '2',
                'clientId': 'C123456',
                'fundId': '2',
                'type': 'CANCELLATION',
                'amount': Decimal('125000'),
                'status': 'COMPLETED'
            }
        ]
        
        mock_transaction_table.query.return_value = {'Items': transactions}
        
        mock_fondo_service.get_fund.side_effect = [
            {'name': 'FPV_EL CLIENTE_RECAUDADORA'},
            {'name': 'FPV_EL CLIENTE_ECOPETROL'}
        ]
        
        # Execute
        result = await TransaccionService.get_client_transactions(client_id, 2)
        
        # Assert
        mock_transaction_table.query.assert_called_once()
        assert len(result) == 2
        assert result[0]['fundName'] == 'FPV_EL CLIENTE_RECAUDADORA'
        assert result[1]['fundName'] == 'FPV_EL CLIENTE_ECOPETROL'
    
    @pytest.mark.asyncio
    async def test_get_client_active_subscriptions_success(
        self, mock_subscription_table, mock_fondo_service
    ):
        # Setup
        client_id = 'C123456'
        subscriptions = [
            {
                'subscriptionId': '1',
                'clientId': 'C123456',
                'fundId': '1',
                'status': 'ACTIVE',
                'amountSubscribed': Decimal('75000')
            },
            {
                'subscriptionId': '2',
                'clientId': 'C123456',
                'fundId': '3',
                'status': 'ACTIVE',
                'amountSubscribed': Decimal('50000')
            }
        ]
        
        mock_subscription_table.query.return_value = {'Items': subscriptions}
        
        mock_fondo_service.get_fund.side_effect = [
            {'name': 'FPV_EL CLIENTE_RECAUDADORA'},
            {'name': 'DEUDAPRIVADA'}
        ]
        
        # Execute
        result = await TransaccionService.get_client_active_subscriptions(client_id)
        
        # Assert
        mock_subscription_table.query.assert_called_once()
        assert len(result) == 2
        assert result[0]['fundName'] == 'FPV_EL CLIENTE_RECAUDADORA'
        assert result[1]['fundName'] == 'DEUDAPRIVADA'
    
    def test_convert_types_for_dynamodb(self):
        # Test conversion of datetime
        test_date = datetime(2025, 3, 28, 12, 0, 0)
        assert convert_types_for_dynamodb(test_date) == '2025-03-28T12:00:00'
        
        # Test conversion of float
        assert convert_types_for_dynamodb(10.5) == Decimal('10.5')
        
        # Test conversion of dict with mixed types
        test_dict = {
            'float_val': 10.5,
            'str_val': 'test',
            'date_val': datetime(2025, 3, 28, 12, 0, 0)
        }
        expected = {
            'float_val': Decimal('10.5'),
            'str_val': 'test',
            'date_val': '2025-03-28T12:00:00'
        }
        assert convert_types_for_dynamodb(test_dict) == expected
        
        # Test conversion of list with mixed types
        test_list = [10.5, 'test', datetime(2025, 3, 28, 12, 0, 0)]
        expected = [Decimal('10.5'), 'test', '2025-03-28T12:00:00']
        assert convert_types_for_dynamodb(test_list) == expected