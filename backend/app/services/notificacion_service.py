import boto3
from botocore.exceptions import ClientError
from app.config import settings



class NotificacionService:
    @staticmethod
    async def send_notification(client_id: str, notification_type: str, message: str, email: str = None, phone: str = None):
        """Envía una notificación por email o SMS según la preferencia del cliente"""
        # enviar una notificación por email o sms dependiendo de la selección del usuario una vez suscrito a dicho fondo
        if notification_type == "email" and email:
            return await NotificacionService.send_email(email, message)
        elif notification_type == "sms" and phone:
            return await NotificacionService.send_sms(phone, message)
        else:
            print(f"No se pudo enviar notificación al cliente {client_id}: datos insuficientes")
            return False

    @staticmethod
    async def send_email(email: str, message: str):
        """Envía un email utilizando Amazon SES"""
        # En un entorno real, usaríamos AWS SES
        # Para esta prueba, solo simulamos el envío
        try:
            print(f"[EMAIL ENVIADO] Destino: {email}, Mensaje: {message}")
            return True
        except Exception as e:
            print(f"Error al enviar email: {str(e)}")
            return False

    @staticmethod
    async def send_sms(phone: str, message: str):
        """Envía un SMS utilizando Amazon SNS"""
        # En un entorno real, usaríamos AWS SNS
        # Para esta prueba, solo simulamos el envío
        try:
            print(f"[SMS ENVIADO] Destino: {phone}, Mensaje: {message}")
            return True
        except Exception as e:
            print(f"Error al enviar SMS: {str(e)}")
            return False