import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from app.main import app

client = TestClient(app)

class TestClienteAPI:
    
    @patch('app.api.endpoints.cliente.ClienteService')
    def test_get_client_success(self, mock_service):
        # Setup
        mock_service.get_client = AsyncMock(return_value={
            'clientId': 'C123456',
            'balance': 500000,
            'preferredNotification': 'email',
            'email': 'cliente@ejemplo.com',
            'phone': '+573001234567'
        })
        
        # Execute
        response = client.get("/api/v1/clientes/C123456")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data['clientId'] == 'C123456'
        assert data['balance'] == 500000
        assert data['preferredNotification'] == 'email'
    
    @patch('app.api.endpoints.cliente.ClienteService')
    def test_get_client_not_found(self, mock_service):
        # Setup
        mock_service.get_client = AsyncMock(return_value=None)
        
        # Execute
        response = client.get("/api/v1/clientes/C999999")
        
        # Assert
        assert response.status_code == 404
        assert response.json()['detail'] == "Cliente no encontrado"
    
    @patch('app.api.endpoints.cliente.ClienteService')
    def test_update_client_success(self, mock_service):
        # Setup
        mock_service.update_client_preferences = AsyncMock(return_value={
            'preferredNotification': 'sms',
            'phone': '+573009876543'
        })
        
        # Execute
        response = client.patch(
            "/api/v1/clientes/C123456",
            json={"preferredNotification": "sms", "phone": "+573009876543"}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data['preferredNotification'] == 'sms'
        assert data['phone'] == '+573009876543'
    
    @patch('app.api.endpoints.cliente.ClienteService')
    def test_update_client_not_found(self, mock_service):
        # Setup
        mock_service.update_client_preferences = AsyncMock(return_value=None)
        
        # Execute
        response = client.patch(
            "/api/v1/clientes/C999999",
            json={"preferredNotification": "sms"}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()['detail'] == "Cliente no encontrado o error al actualizar"

