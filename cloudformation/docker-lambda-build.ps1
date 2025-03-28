# PowerShell script para empaquetar backend con Docker
# Este script garantiza compatibilidad perfecta con AWS Lambda

# Variables
$BACKEND_DIR = (Resolve-Path -Path "..\backend").Path
$DEPLOYMENT_DIR = (Resolve-Path -Path "..\deployment\backend").Path
$DOCKER_IMAGE = "public.ecr.aws/sam/build-python3.9"
$LAMBDA_HANDLER_CONTENT = @"
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

# Verificar si Docker está disponible
try {
    $dockerVersion = docker --version
    Write-Host "Docker encontrado: $dockerVersion" -ForegroundColor Green
}
catch {
    Write-Host "ERROR: Docker no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "Por favor instala Docker Desktop desde: https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
    exit 1
}

# Crear archivo lambda_handler.py en el directorio del backend
Set-Content -Path "$BACKEND_DIR\lambda_handler.py" -Value $LAMBDA_HANDLER_CONTENT

# Crear directorio temporal para el build de Docker
$tempDir = Join-Path -Path $BACKEND_DIR -ChildPath "temp_docker_build"
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

# Copiar los archivos necesarios al directorio temporal
try {
    Copy-Item -Path "$BACKEND_DIR\requirements.txt" -Destination $tempDir
    Copy-Item -Path "$BACKEND_DIR\app" -Destination $tempDir -Recurse
    Copy-Item -Path "$BACKEND_DIR\lambda_handler.py" -Destination $tempDir
    
    # Crear Dockerfile en el directorio temporal
    $dockerfileContent = @"
FROM $DOCKER_IMAGE

WORKDIR /var/task

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt --target ./python
RUN pip install mangum --target ./python

COPY app/ ./python/app/
COPY lambda_handler.py ./python/

# Limpiar archivos innecesarios para reducir tamaño
WORKDIR /var/task/python
RUN find . -type d -name "__pycache__" -exec rm -rf {} +
RUN find . -type d -name "*.dist-info" -exec rm -rf {} +
RUN find . -type d -name "*.egg-info" -exec rm -rf {} +
RUN find . -type d -name "tests" -exec rm -rf {} +

# Comando a ejecutar cuando se inicie el contenedor
CMD ["bash", "-c", "zip -r /output/lambda-package.zip ."]
"@
    Set-Content -Path "$tempDir\Dockerfile" -Value $dockerfileContent
    Write-Host "Archivos preparados para el empaquetado" -ForegroundColor Green

    # Construir la imagen Docker
    Write-Host "Construyendo imagen Docker para Lambda packaging..." -ForegroundColor Cyan
    Push-Location -Path $tempDir
    docker build -t lambda-builder .

    # Ejecutar el contenedor para crear el paquete
    Write-Host "Ejecutando contenedor para crear el paquete Lambda..." -ForegroundColor Cyan
    
    # Asegurarse de que el directorio de salida existe
    if (-not (Test-Path $DEPLOYMENT_DIR)) {
        New-Item -ItemType Directory -Force -Path $DEPLOYMENT_DIR | Out-Null
    }
    
    docker run --rm -v "${DEPLOYMENT_DIR}:/output" lambda-builder
    
    Pop-Location
    
    # Verificar que el archivo ZIP se creó correctamente
    if (Test-Path "$DEPLOYMENT_DIR\lambda-package.zip") {
        Write-Host "Paquete Lambda creado exitosamente: $DEPLOYMENT_DIR\lambda-package.zip" -ForegroundColor Green
    } else {
        Write-Host "ERROR: No se pudo crear el paquete Lambda" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "ERROR durante el empaquetado: $_" -ForegroundColor Red
    exit 1
}
finally {
    # Limpiar archivos temporales
    if (Test-Path $tempDir) {
        Remove-Item -Path $tempDir -Recurse -Force
    }
    if (Test-Path "$BACKEND_DIR\lambda_handler.py") {
        Remove-Item -Path "$BACKEND_DIR\lambda_handler.py" -Force
    }
}

Write-Host "Empaquetado Lambda completado exitosamente!" -ForegroundColor Green