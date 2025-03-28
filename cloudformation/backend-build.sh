#!/bin/bash
set -e

# Crear directorio para el paquete
mkdir -p deployment/backend

# Entrar al directorio del backend
cd backend

# Crear entorno virtual y activarlo
python -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Instalar dependencias adicionales para Lambda
pip install mangum  # Adaptador para ASGI en Lambda

# Crear directorio para el paquete de despliegue
mkdir -p package

# Copiar código de la aplicación
cp -r app package/

# Crear archivo lambda_handler.py que actúa como punto de entrada para Lambda
cat > package/lambda_handler.py << EOL
from mangum import Mangum
from app.main import app

# Crear manejador para Lambda
handler = Mangum(app)
EOL

# Instalar dependencias en el directorio del paquete
pip install -t package/ -r requirements.txt mangum

# Remover archivos innecesarios para reducir tamaño
find package -type d -name "__pycache__" -exec rm -rf {} +
find package -type d -name "*.dist-info" -exec rm -rf {} +
find package -type d -name "*.egg-info" -exec rm -rf {} +
find package -type d -name "tests" -exec rm -rf {} +

# Crear archivo ZIP
cd package
zip -r ../../deployment/backend/lambda-package.zip .

# Desactivar entorno virtual
deactivate

echo "Backend package created at deployment/backend/lambda-package.zip"