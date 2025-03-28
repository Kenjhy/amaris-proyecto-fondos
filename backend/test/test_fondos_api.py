import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock 
from app.main import app

client = TestClient(app)

class TestFondosAPI:
    
    @patch('app.api.endpoints.fondos.FondoService')
    def test_get_all_funds_success(self, mock_service):
        # Setup
        mock_funds = [
            {
                'fundId': '1',
                'name': 'FPV_EL CLIENTE_RECAUDADORA',
                'category': 'FPV',
                'minimumAmount': 75000
            },
            {
                'fundId': '2',
                'name': 'FPV_EL CLIENTE_ECOPETROL',
                'category': 'FPV',
                'minimumAmount': 125000
            }
        ]
        mock_service.get_all_funds = AsyncMock(return_value=mock_funds)
        
        # Execute
        response = client.get("/api/v1/fondos")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]['fundId'] == '1'
        assert data[1]['fundId'] == '2'
    
    @patch('app.api.endpoints.fondos.FondoService')
    def test_get_all_funds_empty(self, mock_service):
        # Setup
        mock_service.get_all_funds = AsyncMock(return_value=[])
        
        # Execute
        response = client.get("/api/v1/fondos")
        
        # Assert
        assert response.status_code == 200
        assert response.json() == []
    
    @patch('app.api.endpoints.fondos.FondoService')
    def test_get_fund_success(self, mock_service):
        # Setup
        mock_fund = {
            'fundId': '1',
            'name': 'FPV_EL CLIENTE_RECAUDADORA',
            'category': 'FPV',
            'minimumAmount': 75000
        }
        mock_service.get_fund = AsyncMock(return_value=mock_fund)
        
        # Execute
        response = client.get("/api/v1/fondos/1")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data['fundId'] == '1'
        assert data['name'] == 'FPV_EL CLIENTE_RECAUDADORA'
    
    @patch('app.api.endpoints.fondos.FondoService')
    def test_get_fund_not_found(self, mock_service):
        # Setup
        mock_service.get_fund = AsyncMock(return_value=None)
        
        # Execute
        response = client.get("/api/v1/fondos/999")
        
        # Assert
        assert response.status_code == 404
        assert response.json()['detail'] == "Fondo no encontrado"