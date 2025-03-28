#!/bin/bash
set -e

# Crear directorio para el paquete
mkdir -p deployment/frontend

# Entrar al directorio del frontend
cd frontend

# Instalar dependencias
npm install

# Agregar configuración para apuntar a la API en producción
cat > .env.production << EOL
# Este archivo será usado cuando ejecutes 'npm run build'
REACT_APP_API_URL=https://YOUR_API_ID.execute-api.YOUR_REGION.amazonaws.com/prod/api/v1
EOL

# Construir la aplicación
npm run build

# Copiar archivos de compilación al directorio de despliegue
cp -r build/* ../deployment/frontend/

echo "Frontend build created at deployment/frontend/"