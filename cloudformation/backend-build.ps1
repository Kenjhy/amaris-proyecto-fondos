# PowerShell script para empaquetar backend
# Crear directorios para el paquete
New-Item -ItemType Directory -Force -Path ..\deployment\backend | Out-Null

# Entrar al directorio del backend
Push-Location -Path ..\backend

# Limpiar directorio de paquete si existe
if (Test-Path .\package) {
    Remove-Item -Recurse -Force .\package
}
New-Item -ItemType Directory -Force -Path .\package | Out-Null

# Usar un entorno de Python limpio
if (Test-Path .\venv) {
    Remove-Item -Recurse -Force .\venv
}

Write-Host "Creando y activando entorno virtual..."
python -m venv venv
.\venv\Scripts\Activate.ps1

# Instalar dependencias
Write-Host "Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt
pip install mangum

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

# Instalar todas las dependencias directamente en el directorio del paquete
# Este es un enfoque más directo que evita problemas de dependencias
Write-Host "Instalando dependencias en el paquete..."
pip install -t .\package\ --no-deps mangum
pip install -t .\package\ -r requirements.txt
pip install -t .\package\ email-validator==2.2.0 dnspython==2.7.0

# Dependencias específicas que a menudo causan problemas
Write-Host "Instalando dependencias críticas..."
pip install -t .\package\ pydantic==2.10.6 pydantic-core==2.27.2 typing-extensions==4.13.0

# Limpiar archivos innecesarios para reducir tamaño
Write-Host "Limpiando archivos innecesarios..."
Get-ChildItem -Path .\package -Include __pycache__ -Recurse -Directory | Remove-Item -Recurse -Force
Get-ChildItem -Path .\package -Include *.dist-info -Recurse -Directory | Remove-Item -Recurse -Force
Get-ChildItem -Path .\package -Include *.egg-info -Recurse -Directory | Remove-Item -Recurse -Force
Get-ChildItem -Path .\package -Include tests -Recurse -Directory | Remove-Item -Recurse -Force

# Crear archivo ZIP
Write-Host "Creando archivo ZIP..."
$deploymentPath = (Resolve-Path ..\deployment\backend).Path
Push-Location -Path .\package
Compress-Archive -Path * -DestinationPath "$deploymentPath\lambda-package.zip" -Force
Pop-Location

# Desactivar entorno virtual
deactivate

# Volver al directorio original
Pop-Location

Write-Host "Backend package creado en deployment/backend/lambda-package.zip"