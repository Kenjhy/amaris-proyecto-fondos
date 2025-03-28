import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from app.main import app

client = TestClient(app)

class TestTransaccionesAPI:
    
    @patch('app.api.endpoints.transacciones.TransaccionService')
    def test_create_subscription_success(self, mock_service):
        # Setup
        mock_result = {
            'transactionId': '1234',
            'clientId': 'C123456',
            'fundId': '1',
            'type': 'SUBSCRIPTION',
            'amount': 75000,
            'status': 'COMPLETED',
            'fundName': 'FPV_EL CLIENTE_RECAUDADORA'
        }
        mock_service.create_subscription = AsyncMock(return_value=mock_result)
        
        # Execute
        response = client.post(
            "/api/v1/transacciones/subscriptions",
            json={"fundId": "1"}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data['transactionId'] == '1234'
        assert data['type'] == 'SUBSCRIPTION'
        assert data['status'] == 'COMPLETED'
        assert data['fundName'] == 'FPV_EL CLIENTE_RECAUDADORA'
    
    @patch('app.api.endpoints.transacciones.TransaccionService')
    def test_create_subscription_error(self, mock_service):
        # Setup
        mock_result = {
            'error': 'No tiene saldo disponible para vincularse al fondo',
            'status': 'FAILED'
        }
        mock_service.create_subscription = AsyncMock(return_value=mock_result)
        
        # Execute
        response = client.post(
            "/api/v1/transacciones/subscriptions",
            json={"fundId": "1"}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()['detail'] == 'No tiene saldo disponible para vincularse al fondo'
    
    @patch('app.api.endpoints.transacciones.TransaccionService')
    def test_cancel_subscription_success(self, mock_service):
        # Setup
        mock_result = {
            'transactionId': '1234',
            'clientId': 'C123456',
            'fundId': '1',
            'type': 'CANCELLATION',
            'amount': 75000,
            'status': 'COMPLETED',
            'fundName': 'FPV_EL CLIENTE_RECAUDADORA'
        }
        mock_service.cancel_subscription = AsyncMock(return_value=mock_result)
        
        # Execute
        response = client.delete("/api/v1/transacciones/subscriptions/1")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data['transactionId'] == '1234'
        assert data['type'] == 'CANCELLATION'
        assert data['status'] == 'COMPLETED'
    
    @patch('app.api.endpoints.transacciones.TransaccionService')
    def test_cancel_subscription_error(self, mock_service):
        # Setup
        mock_result = {
            'error': 'No está suscrito a este fondo',
            'status': 'FAILED'
        }
        mock_service.cancel_subscription = AsyncMock(return_value=mock_result)
        
        # Execute
        response = client.delete("/api/v1/transacciones/subscriptions/999")
        
        # Assert
        assert response.status_code == 400
        assert response.json()['detail'] == 'No está suscrito a este fondo'
    
    @patch('app.api.endpoints.transacciones.TransaccionService')
    def test_get_transactions_history_success(self, mock_service):
        # Setup
        mock_transactions = [
            {
                'transactionId': '1',
                'clientId': 'C123456',
                'fundId': '1',
                'type': 'SUBSCRIPTION',
                'amount': 75000,
                'status': 'COMPLETED',
                'fundName': 'FPV_EL CLIENTE_RECAUDADORA'
            },
            {
                'transactionId': '2',
                'clientId': 'C123456',
                'fundId': '2',
                'type': 'CANCELLATION',
                'amount': 125000,
                'status': 'COMPLETED',
                'fundName': 'FPV_EL CLIENTE_ECOPETROL'
            }
        ]
        mock_service.get_client_transactions = AsyncMock(return_value=mock_transactions)
        
        # Execute
        response = client.get("/api/v1/transacciones/history?limit=2")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]['transactionId'] == '1'
        assert data[1]['transactionId'] == '2'
    
    @patch('app.api.endpoints.transacciones.TransaccionService')
    def test_get_active_subscriptions_success(self, mock_service):
        # Setup
        mock_subscriptions = [
            {
                'subscriptionId': '1',
                'clientId': 'C123456',
                'fundId': '1',
                'status': 'ACTIVE',
                'amountSubscribed': 75000,
                'fundName': 'FPV_EL CLIENTE_RECAUDADORA'
            }
        ]
        mock_service.get_client_active_subscriptions = AsyncMock(return_value=mock_subscriptions)
        
        # Execute
        response = client.get("/api/v1/transacciones/subscriptions")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['subscriptionId'] == '1'
        assert data[0]['status'] == 'ACTIVE'
        assert data[0]['fundName'] == 'FPV_EL CLIENTE_RECAUDADORA'
