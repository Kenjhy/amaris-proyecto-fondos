# PowerShell script para construir frontend
# Crear directorio para el paquete
New-Item -ItemType Directory -Force -Path ..\deployment\frontend | Out-Null

# Entrar al directorio del frontend
Push-Location -Path ..\frontend

# Instalar dependencias
Write-Host "Instalando dependencias NPM..."
npm install

# Agregar configuración para apuntar a la API en producción
$envContent = @"
# Este archivo será usado cuando ejecutes 'npm run build'
REACT_APP_API_URL=https://YOUR_API_ID.execute-api.YOUR_REGION.amazonaws.com/prod/api/v1
"@
Set-Content -Path .\.env.production -Value $envContent

# Construir la aplicación
Write-Host "Construyendo la aplicación..."
npm run build

# Copiar archivos de compilación al directorio de despliegue
Write-Host "Copiando archivos a directorio de despliegue..."
Copy-Item -Path .\build\* -Destination ..\deployment\frontend -Recurse -Force

# Volver al directorio original
Pop-Location

Write-Host "Frontend build creado en deployment/frontend/"