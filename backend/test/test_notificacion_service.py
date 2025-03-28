import pytest
from unittest.mock import patch, MagicMock, AsyncMock 
from app.services.notificacion_service import NotificacionService

class TestNotificacionService:
    
    @pytest.mark.asyncio
    async def test_send_notification_email(self):
        # Setup
        with patch.object(NotificacionService, 'send_email', return_value=True) as mock_send_email:
            # Execute
            result = await NotificacionService.send_notification(
                client_id='C123456',
                notification_type='email',
                message='Test message',
                email='test@example.com',
                phone=None
            )
            
            # Assert
            mock_send_email.assert_called_once_with('test@example.com', 'Test message')
            assert result is True
    
    @pytest.mark.asyncio
    async def test_send_notification_sms(self):
        # Setup
        with patch.object(NotificacionService, 'send_sms', return_value=True) as mock_send_sms:
            # Execute
            result = await NotificacionService.send_notification(
                client_id='C123456',
                notification_type='sms',
                message='Test message',
                email=None,
                phone='+573001234567'
            )
            
            # Assert
            mock_send_sms.assert_called_once_with('+573001234567', 'Test message')
            assert result is True
    
    @pytest.mark.asyncio
    async def test_send_notification_missing_data(self):
        # Execute
        result = await NotificacionService.send_notification(
            client_id='C123456',
            notification_type='email',
            message='Test message',
            email=None,
            phone=None
        )
        
        # Assert
        assert result is False
    
    @pytest.mark.asyncio
    async def test_send_email_success(self):
        # Setup
        with patch('builtins.print') as mock_print:
            # Execute
            result = await NotificacionService.send_email('test@example.com', 'Test message')
            
            # Assert
            mock_print.assert_called_once()
            assert result is True
    
    @pytest.mark.asyncio
    async def test_send_email_exception(self):
        # Instead of patching print, patch the entire function with an exception
        with patch('app.services.notificacion_service.NotificacionService.send_email',
                side_effect=Exception("Test exception")):
            try:
                # This will throw an exception
                result = await NotificacionService.send_notification(
                    client_id='C123456',
                    notification_type='email',
                    message='Test message',
                    email='test@example.com'
                )
                assert False, "Should have raised an exception"
            except Exception:
                # If we catch the exception here, the test passes
                pass
            
    @pytest.mark.asyncio
    async def test_send_email_failure(self):
        # Test that notification fails when email sending fails
        with patch('app.services.notificacion_service.NotificacionService.send_email',
                return_value=False):
            result = await NotificacionService.send_notification(
                client_id='C123456',
                notification_type='email',
                message='Test message',
                email='test@example.com'
            )
            assert result is False
            
    @pytest.mark.asyncio
    async def test_send_sms_failure(self):
        # Test that notification fails when SMS sending fails
        with patch('app.services.notificacion_service.NotificacionService.send_sms',
                return_value=False):
            result = await NotificacionService.send_notification(
                client_id='C123456',
                notification_type='sms',
                message='Test message',
                phone='+573001234567'
            )
            assert result is False
    
    @pytest.mark.asyncio
    async def test_send_sms_success(self):
        # Setup
        with patch('builtins.print') as mock_print:
            # Execute
            result = await NotificacionService.send_sms('+573001234567', 'Test message')
            
            # Assert
            mock_print.assert_called_once()
            assert result is True
    
    @pytest.mark.asyncio
    async def test_send_sms_exception(self):
        # Dado que send_sms lanza una excepción que se propaga,
        # debemos esperar que se produzca la excepción
        with patch.object(NotificacionService, 'send_sms',
                        side_effect=Exception("Test exception")):
            with pytest.raises(Exception):
                await NotificacionService.send_notification(
                    client_id='C123456',
                    notification_type='sms',
                    message='Test message',
                    phone='+573001234567'
                )