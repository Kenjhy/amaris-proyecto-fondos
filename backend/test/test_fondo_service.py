import pytest
import boto3
from decimal import Decimal
from unittest.mock import patch, MagicMock, AsyncMock 
from app.services.fondo_service import FondoService

@pytest.fixture
def mock_dynamodb_table():
    with patch('app.services.fondo_service.table') as mock_table:
        yield mock_table

@pytest.fixture
def sample_funds_data():
    return [
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
        }
    ]

class TestFondoService:
    
    @pytest.mark.asyncio
    async def test_get_all_funds_success(self, mock_dynamodb_table, sample_funds_data):
        # Setup
        mock_dynamodb_table.scan.return_value = {'Items': sample_funds_data}
        
        # Execute
        result = await FondoService.get_all_funds()
        
        # Assert
        mock_dynamodb_table.scan.assert_called_once()
        assert result == sample_funds_data
    
    @pytest.mark.asyncio
    async def test_get_all_funds_empty(self, mock_dynamodb_table):
        # Setup
        mock_dynamodb_table.scan.return_value = {'Items': []}
        
        # Execute
        result = await FondoService.get_all_funds()
        
        # Assert
        mock_dynamodb_table.scan.assert_called_once()
        assert result == []
    
    @pytest.mark.asyncio
    async def test_get_all_funds_error(self, mock_dynamodb_table):
        # Setup
        from botocore.exceptions import ClientError
        error_response = {'Error': {'Message': 'Test error message'}}
        mock_dynamodb_table.scan.side_effect = ClientError(error_response, 'Scan')
        
        # Execute
        result = await FondoService.get_all_funds()
        
        # Assert
        mock_dynamodb_table.scan.assert_called_once()
        assert result == []
    
    @pytest.mark.asyncio
    async def test_get_fund_success(self, mock_dynamodb_table, sample_funds_data):
        # Setup
        mock_dynamodb_table.get_item.return_value = {'Item': sample_funds_data[0]}
        
        # Execute
        result = await FondoService.get_fund('1')
        
        # Assert
        mock_dynamodb_table.get_item.assert_called_once_with(Key={'fundId': '1'})
        assert result == sample_funds_data[0]
    
    @pytest.mark.asyncio
    async def test_get_fund_not_found(self, mock_dynamodb_table):
        # Setup
        mock_dynamodb_table.get_item.return_value = {}
        
        # Execute
        result = await FondoService.get_fund('999')
        
        # Assert
        mock_dynamodb_table.get_item.assert_called_once_with(Key={'fundId': '999'})
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_fund_error(self, mock_dynamodb_table):
        # Setup
        from botocore.exceptions import ClientError
        error_response = {'Error': {'Message': 'Test error message'}}
        mock_dynamodb_table.get_item.side_effect = ClientError(error_response, 'GetItem')
        
        # Execute
        result = await FondoService.get_fund('1')
        
        # Assert
        mock_dynamodb_table.get_item.assert_called_once_with(Key={'fundId': '1'})
        assert result is None