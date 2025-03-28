# PowerShell script para empaquetar backend usando Docker para la compatibilidad con Lambda
# Crear directorios para el paquete
New-Item -ItemType Directory -Force -Path ..\deployment\backend | Out-Null
New-Item -ItemType Directory -Force -Path ..\deployment\layers | Out-Null

# Entrar al directorio del backend
Push-Location -Path ..\backend

# Limpiar directorio de paquete si existe
if (Test-Path .\package) {
    Remove-Item -Recurse -Force .\package
}
New-Item -ItemType Directory -Force -Path .\package | Out-Null

# Crear archivo temporal con versiones flexibles de las dependencias
$flexibleRequirements = @"
annotated-types>=0.7.0
anyio>=4.9.0
boto3>=1.37.21
botocore>=1.37.21
certifi>=2025.1.31
click>=8.1.8
colorama>=0.4.6
dnspython>=2.7.0
ecdsa>=0.19.1
email_validator>=2.2.0
fastapi>=0.115.12
h11>=0.14.0
httpcore>=1.0.7
httpx>=0.28.1
idna>=3.10
iniconfig>=2.1.0
jmespath>=1.0.1
packaging>=24.2
pluggy>=1.5.0
pyasn1>=0.4.8
pydantic>=2.10.6
pydantic-settings>=2.8.1
pydantic_core>=2.27.2
pytest>=8.3.5
pytest-asyncio>=0.26.0
python-dateutil>=2.9.0
python-dotenv>=1.1.0
python-jose>=3.4.0
rsa>=4.9
s3transfer>=0.11.4
six>=1.17.0
sniffio>=1.3.1
starlette>=0.46.1
typing_extensions>=4.13.0
urllib3>=1.25.4,<1.27
uvicorn>=0.34.0
"@

# Guardar el archivo temporal
Set-Content -Path .\flexible-requirements.txt -Value $flexibleRequirements

# Crear una imagen Docker para compilar las dependencias en un entorno Linux compatible con Lambda
$dockerFileContent = @"
FROM public.ecr.aws/lambda/python:3.9

# Instalar zip
RUN yum install -y zip

# Copiar requirements flexibles
COPY flexible-requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -t /python -r flexible-requirements.txt
RUN pip install --no-cache-dir -t /python mangum==0.19.0

# Comprimir las dependencias
RUN mkdir -p /output/python
RUN cp -r /python/* /output/python/
RUN cd /output && zip -r layer.zip python
"@

# Crear archivo Dockerfile
Set-Content -Path .\Dockerfile -Value $dockerFileContent

# Construir imagen Docker y ejecutar contenedor para crear layer
Write-Host "Construyendo imagen Docker para crear layer compatible con Lambda..."
docker build -t lambda-layer-builder .
docker run --name lambda-layer-container lambda-layer-builder
docker cp lambda-layer-container:/output/layer.zip ..\deployment\layers\python-dependencies.zip
docker rm lambda-layer-container

# Crear archivo lambda_handler.py con logging para debugging
$lambdaHandlerContent = @"
from mangum import Mangum
from app.main import app
import logging
import sys

# Configurar logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Informar sobre el entorno
logger.info(f"Python version: {sys.version}")
logger.info(f"Python path: {sys.path}")

# Crear manejador para Lambda
handler = Mangum(app, lifespan="off")
"@
Set-Content -Path .\package\lambda_handler.py -Value $lambdaHandlerContent

# Copiar código de la aplicación
Write-Host "Copiando código de la aplicación..."
Copy-Item -Path .\app -Destination .\package -Recurse

# Limpiar archivos innecesarios para reducir tamaño
Write-Host "Limpiando archivos innecesarios..."
Get-ChildItem -Path .\package -Include __pycache__ -Recurse -Directory | Remove-Item -Recurse -Force

# Crear archivo ZIP del código de la aplicación (sin dependencias)
Write-Host "Creando archivo ZIP..."
$deploymentPath = (Resolve-Path ..\deployment\backend).Path
Push-Location -Path .\package
Compress-Archive -Path * -DestinationPath "$deploymentPath\lambda-package.zip" -Force
Pop-Location

# Limpiar archivos temporales
Remove-Item -Force .\flexible-requirements.txt -ErrorAction SilentlyContinue
Remove-Item -Force .\Dockerfile -ErrorAction SilentlyContinue

# Volver al directorio original
Pop-Location

Write-Host "Backend package creado en deployment/backend/lambda-package.zip"
Write-Host "Layer de dependencias creado en deployment/layers/python-dependencies.zip"