import pytest
import boto3
import uuid
from decimal import Decimal
from unittest.mock import patch, MagicMock, AsyncMock  
from app.models.cliente import Cliente, ClienteUpdate
from app.services.cliente_service import ClienteService, float_to_decimal

# Mocking the DynamoDB table operations
@pytest.fixture
def mock_dynamodb_table():
    with patch('app.services.cliente_service.table') as mock_table:
        yield mock_table

@pytest.fixture
def sample_client_data():
    return {
        'clientId': 'C123456',
        'balance': Decimal('500000'),
        'preferredNotification': 'email',
        'email': 'cliente@ejemplo.com',
        'phone': '+573001234567'
    }

class TestClienteService:
    
    @pytest.mark.asyncio
    async def test_get_client_success(self, mock_dynamodb_table, sample_client_data):
        # Setup
        mock_dynamodb_table.get_item.return_value = {'Item': sample_client_data}
        
        # Execute
        result = await ClienteService.get_client('C123456')
        
        # Assert
        mock_dynamodb_table.get_item.assert_called_once_with(Key={'clientId': 'C123456'})
        assert result == sample_client_data
    
    @pytest.mark.asyncio
    async def test_get_client_not_found(self, mock_dynamodb_table):
        # Setup
        mock_dynamodb_table.get_item.return_value = {}
        
        # Execute
        result = await ClienteService.get_client('C999999')
        
        # Assert
        mock_dynamodb_table.get_item.assert_called_once_with(Key={'clientId': 'C999999'})
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_client_error(self, mock_dynamodb_table):
        # Setup
        from botocore.exceptions import ClientError
        error_response = {'Error': {'Message': 'Test error message'}}
        mock_dynamodb_table.get_item.side_effect = ClientError(error_response, 'GetItem')
        
        # Execute
        result = await ClienteService.get_client('C123456')
        
        # Assert
        mock_dynamodb_table.get_item.assert_called_once_with(Key={'clientId': 'C123456'})
        assert result is None
    
    @pytest.mark.asyncio
    async def test_update_client_balance_success(self, mock_dynamodb_table):
        # Setup
        mock_dynamodb_table.update_item.return_value = {
            'Attributes': {'balance': Decimal('600000')}
        }
        
        # Execute
        result = await ClienteService.update_client_balance('C123456', 100000)
        
        # Assert
        mock_dynamodb_table.update_item.assert_called_once()
        assert result == {'balance': Decimal('600000')}
    
    @pytest.mark.asyncio
    async def test_update_client_balance_error(self, mock_dynamodb_table):
        # Setup
        from botocore.exceptions import ClientError
        error_response = {'Error': {'Message': 'Test error message'}}
        mock_dynamodb_table.update_item.side_effect = ClientError(error_response, 'UpdateItem')
        
        # Execute
        result = await ClienteService.update_client_balance('C123456', 100000)
        
        # Assert
        mock_dynamodb_table.update_item.assert_called_once()
        assert result is None
    
    @pytest.mark.asyncio
    async def test_update_client_preferences_all_fields(self, mock_dynamodb_table):
        # Setup
        update_data = ClienteUpdate(
            preferredNotification='sms',
            email='nuevo@ejemplo.com',
            phone='+573009876543'
        )
        mock_dynamodb_table.update_item.return_value = {
            'Attributes': {
                'preferredNotification': 'sms',
                'email': 'nuevo@ejemplo.com',
                'phone': '+573009876543'
            }
        }
        
        # Execute
        result = await ClienteService.update_client_preferences('C123456', update_data)
        
        # Assert
        mock_dynamodb_table.update_item.assert_called_once()
        assert 'preferredNotification = :notification' in mock_dynamodb_table.update_item.call_args[1]['UpdateExpression']
        assert 'email = :email' in mock_dynamodb_table.update_item.call_args[1]['UpdateExpression']
        assert 'phone = :phone' in mock_dynamodb_table.update_item.call_args[1]['UpdateExpression']
        assert result == {
            'preferredNotification': 'sms',
            'email': 'nuevo@ejemplo.com',
            'phone': '+573009876543'
        }
    
    @pytest.mark.asyncio
    async def test_update_client_preferences_partial(self, mock_dynamodb_table):
        # Setup
        update_data = ClienteUpdate(preferredNotification='sms')
        mock_dynamodb_table.update_item.return_value = {
            'Attributes': {'preferredNotification': 'sms'}
        }
        
        # Execute
        result = await ClienteService.update_client_preferences('C123456', update_data)
        
        # Assert
        mock_dynamodb_table.update_item.assert_called_once()
        assert 'preferredNotification = :notification' in mock_dynamodb_table.update_item.call_args[1]['UpdateExpression']
        assert 'email = :email' not in mock_dynamodb_table.update_item.call_args[1]['UpdateExpression']
        assert 'phone = :phone' not in mock_dynamodb_table.update_item.call_args[1]['UpdateExpression']
        assert result == {'preferredNotification': 'sms'}
    
    @pytest.mark.asyncio
    async def test_update_client_preferences_error(self, mock_dynamodb_table):
        # Setup
        update_data = ClienteUpdate(preferredNotification='sms')
        from botocore.exceptions import ClientError
        error_response = {'Error': {'Message': 'Test error message'}}
        mock_dynamodb_table.update_item.side_effect = ClientError(error_response, 'UpdateItem')
        
        # Execute
        result = await ClienteService.update_client_preferences('C123456', update_data)
        
        # Assert
        mock_dynamodb_table.update_item.assert_called_once()
        assert result is None
    
    def test_float_to_decimal_conversion(self):
        # Test conversion of float
        assert float_to_decimal(10.5) == Decimal('10.5')
        
        # Test conversion of dict with float
        input_dict = {'a': 10.5, 'b': 'string', 'c': 100}
        expected = {'a': Decimal('10.5'), 'b': 'string', 'c': 100}
        assert float_to_decimal(input_dict) == expected
        
        # Test conversion of list with float
        input_list = [10.5, 'string', 100]
        expected = [Decimal('10.5'), 'string', 100]
        assert float_to_decimal(input_list) == expected
        
        # Test with nested structures
        nested = {'a': [10.5, 20.5], 'b': {'c': 30.5}}
        expected = {'a': [Decimal('10.5'), Decimal('20.5')], 'b': {'c': Decimal('30.5')}}
        assert float_to_decimal(nested) == expected
