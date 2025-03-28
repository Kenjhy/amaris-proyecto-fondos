from mangum import Mangum
from app.main import app
import logging

# Configurar logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Crear manejador para Lambda con mejores configuraciones
handler = Mangum(app, lifespan="off")


# Agregar un wrapper para capturar errores
def lambda_handler(event, context):
    logger.info(f"Evento recibido: {event}")
    try:
        return handler(event, context)
    except Exception as e:
        logger.error(f"Error en Lambda handler: {str(e)}")
        return {
            "statusCode": 500,
            "body": '{"message": "Error interno del servidor - ' + str(e) + '"}'
        }