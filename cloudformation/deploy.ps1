# Script PowerShell para despliegue en AWS CloudFormation

# Variables configurables
$STACK_NAME = "ElCliente-Stack"
$REGION = "us-east-1"  # Cambia según tu región preferida
$STAGE = "prod"

# Colores para mensajes
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    else {
        $input | Write-Output
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

Write-ColorOutput Yellow "Iniciando despliegue de la aplicación El Cliente - Fondos"

# Verificar AWS CLI
try {
    aws --version
}
catch {
    Write-ColorOutput Red "Error: AWS CLI no está instalado"
    Write-Output "Instala AWS CLI siguiendo las instrucciones en: https://aws.amazon.com/cli/"
    exit 1
}

# Verificar credenciales
Write-ColorOutput Yellow "Verificando credenciales de AWS..."
try {
    $identity = aws sts get-caller-identity
    if (-not $identity) {
        throw "No se pudieron obtener las credenciales"
    }
}
catch {
    Write-ColorOutput Red "Error: No se pudieron verificar las credenciales de AWS"
    Write-Output "Configura tus credenciales con 'aws configure' o asegúrate de que estén correctamente configuradas"
    exit 1
}

# Verificar permisos CloudFormation
Write-ColorOutput Yellow "Verificando permisos para CloudFormation..."
try {
    aws cloudformation list-stacks --max-items 1
}
catch {
    Write-ColorOutput Red "Error: No tienes permisos suficientes para CloudFormation"
    Write-Output "Asegúrate de tener los permisos necesarios para CloudFormation"
    exit 1
}

# Eliminar el stack si está en estado ROLLBACK_COMPLETE
try {
    $stack = aws cloudformation describe-stacks --stack-name $STACK_NAME 2>$null | ConvertFrom-Json
    $stackStatus = $stack.Stacks[0].StackStatus
    
    if ($stackStatus -eq "ROLLBACK_COMPLETE") {
        Write-ColorOutput Yellow "El stack está en estado ROLLBACK_COMPLETE. Eliminando stack..."
        aws cloudformation delete-stack --stack-name $STACK_NAME
        Write-ColorOutput Yellow "Esperando a que se elimine el stack..."
        aws cloudformation wait stack-delete-complete --stack-name $STACK_NAME
        Write-ColorOutput Green "Stack eliminado correctamente."
    } else {
        Write-ColorOutput Yellow "Stack existente en estado: $stackStatus"
    }
} catch {
    Write-ColorOutput Yellow "No se encontró stack existente o hubo un error al verificar el estado."
}

# Crear directorio de despliegue si no existe
New-Item -ItemType Directory -Force -Path ..\deployment\backend | Out-Null
New-Item -ItemType Directory -Force -Path ..\deployment\frontend | Out-Null
New-Item -ItemType Directory -Force -Path ..\deployment\layers | Out-Null

# Paso 1: Verificando bucket de despliegue...
Write-ColorOutput Yellow "Paso 1: Verificando bucket de despliegue..."

$ACCOUNT_ID = (aws sts get-caller-identity --query Account --output text)
$DEPLOYMENT_BUCKET = "elcliente-deployment-${ACCOUNT_ID}-${REGION}"

# Verificar si el bucket existe
$bucketExists = $false
try {
    aws s3api head-bucket --bucket $DEPLOYMENT_BUCKET 2>$null
    Write-Output "El bucket de despliegue $DEPLOYMENT_BUCKET ya existe."
    $bucketExists = $true
}
catch {
    # Solicitar al usuario que cree el bucket manualmente
    Write-ColorOutput Red "Error: El bucket $DEPLOYMENT_BUCKET no existe."
    Write-ColorOutput Yellow "Por favor, crea el bucket manualmente desde la consola AWS:"
    Write-ColorOutput Yellow "1. Ve a https://s3.console.aws.amazon.com/s3/"
    Write-ColorOutput Yellow "2. Haz clic en 'Create bucket'"
    Write-ColorOutput Yellow "3. Nombre: $DEPLOYMENT_BUCKET"
    Write-ColorOutput Yellow "4. Desmarca todas las opciones de 'Block Public Access'"
    Write-ColorOutput Yellow "5. Asegúrate de habilitar el versionamiento (opcional)"
    Write-ColorOutput Yellow "6. Completa la creación del bucket"
    
    $confirmation = Read-Host "¿Has creado manualmente el bucket? (s/n)"
    if ($confirmation -ne "s") {
        Write-ColorOutput Red "Despliegue cancelado. Crea el bucket y vuelve a ejecutar el script."
        exit 1
    }
    
    # Verificar nuevamente si el bucket ahora existe
    try {
        aws s3api head-bucket --bucket $DEPLOYMENT_BUCKET 2>$null
        Write-Output "Bucket verificado correctamente."
        $bucketExists = $true
    }
    catch {
        Write-ColorOutput Red "El bucket $DEPLOYMENT_BUCKET sigue sin estar disponible. Verifica que lo hayas creado correctamente."
        exit 1
    }
}

# Paso 2: Empaquetar el backend usando el nuevo script que genera la layer
Write-ColorOutput Yellow "Paso 2: Empaquetando backend..."
& .\backend-build-fixed.ps1

# Paso 3: Empaquetar el frontend
Write-ColorOutput Yellow "Paso 3: Construyendo frontend..."
& .\frontend-build.ps1

# Paso 4: Subir paquetes al bucket S3
Write-ColorOutput Yellow "Paso 4: Subiendo paquetes a S3..."
$backendPackagePath = "..\deployment\backend\lambda-package.zip"
$layerPackagePath = "..\deployment\layers\python-dependencies.zip"

if (Test-Path $backendPackagePath) {
    Write-Output "Subiendo paquete Lambda..."
    try {
        aws s3 cp $backendPackagePath s3://$DEPLOYMENT_BUCKET/backend/lambda-package.zip
        Write-ColorOutput Green "Paquete Lambda subido correctamente."
    }
    catch {
        Write-ColorOutput Red "Error al subir paquete Lambda: $_"
        Write-ColorOutput Yellow "Verificando permisos del bucket..."
        aws s3api get-bucket-acl --bucket $DEPLOYMENT_BUCKET
        Write-ColorOutput Red "Por favor verifica los permisos de tu usuario para acceder al bucket."
        exit 1
    }
}
else {
    Write-ColorOutput Red "Error: No se encuentra el archivo $backendPackagePath"
    exit 1
}

if (Test-Path $layerPackagePath) {
    Write-Output "Subiendo Layer de dependencias..."
    try {
        aws s3 cp $layerPackagePath s3://$DEPLOYMENT_BUCKET/layers/python-dependencies.zip
        Write-ColorOutput Green "Layer de dependencias subido correctamente."
    }
    catch {
        Write-ColorOutput Red "Error al subir layer de dependencias: $_"
        exit 1
    }
}
else {
    Write-ColorOutput Red "Error: No se encuentra el archivo $layerPackagePath"
    exit 1
}

# Paso 5: Desplegar stack de CloudFormation con el parámetro correcto para el bucket
Write-ColorOutput Yellow "Paso 5: Desplegando stack de CloudFormation..."
try {
    # Pasamos el parámetro CreateDeploymentBucket como "false" ya que el bucket existe
    aws cloudformation deploy `
        --template-file .\template.yaml `
        --stack-name $STACK_NAME `
        --parameter-overrides Stage=$STAGE CreateDeploymentBucket="false" `
        --capabilities CAPABILITY_IAM `
        --region $REGION `
        --no-fail-on-empty-changeset
    
    if ($LASTEXITCODE -ne 0) {
        throw "Error en el despliegue de CloudFormation"
    }
    
    Write-ColorOutput Green "Stack desplegado correctamente."
}
catch {
    Write-ColorOutput Red "Error: Falló el despliegue de CloudFormation: $_"
    Write-ColorOutput Yellow "Para más detalles, ejecuta: aws cloudformation describe-stack-events --stack-name $STACK_NAME"
    exit 1
}

# Obtener outputs del stack
Write-ColorOutput Yellow "Obteniendo información del despliegue..."
try {
    $stackOutputs = aws cloudformation describe-stacks --stack-name $STACK_NAME --region $REGION | ConvertFrom-Json
    $FRONTEND_BUCKET = ($stackOutputs.Stacks[0].Outputs | Where-Object { $_.ExportName -eq "$STACK_NAME-FrontendBucket" }).OutputValue
    $API_ENDPOINT = ($stackOutputs.Stacks[0].Outputs | Where-Object { $_.ExportName -eq "$STACK_NAME-ApiEndpoint" }).OutputValue
    $CLOUDFRONT_DOMAIN = ($stackOutputs.Stacks[0].Outputs | Where-Object { $_.ExportName -eq "$STACK_NAME-CloudFrontDomain" }).OutputValue
    
    Write-ColorOutput Green "Información obtenida correctamente."
    if ($FRONTEND_BUCKET) { Write-ColorOutput Yellow "Frontend Bucket: $FRONTEND_BUCKET" }
    if ($API_ENDPOINT) { Write-ColorOutput Yellow "API Endpoint: $API_ENDPOINT" }
    if ($CLOUDFRONT_DOMAIN) { Write-ColorOutput Yellow "CloudFront Domain: $CLOUDFRONT_DOMAIN" }
}
catch {
    Write-ColorOutput Yellow "Aviso: No se pudieron obtener todos los outputs del stack. Continuando..."
}

# Paso 6: Actualizar configuración del frontend con la URL de API correcta
if ($API_ENDPOINT) {
    Write-ColorOutput Yellow "Paso 6: Actualizando configuración del frontend..."
    try {
        Set-Content -Path ..\frontend\.env.production -Value "REACT_APP_API_URL=$API_ENDPOINT/api/v1"
        Push-Location -Path ..\frontend
        npm run build
        Pop-Location
        Write-ColorOutput Green "Frontend configurado y construido correctamente."
    }
    catch {
        Write-ColorOutput Red "Error al configurar o construir el frontend: $_"
    }
}

# Paso 7: Subir frontend a S3
if ($FRONTEND_BUCKET) {
    Write-ColorOutput Yellow "Paso 7: Desplegando frontend a S3..."
    $frontendBuildPath = "..\frontend\build\"
    if (Test-Path $frontendBuildPath) {
        try {
            aws s3 sync $frontendBuildPath s3://$FRONTEND_BUCKET/ --delete
            Write-ColorOutput Green "Frontend desplegado correctamente en S3."
        }
        catch {
            Write-ColorOutput Red "Error al desplegar frontend en S3: $_"
        }
    }
    else {
        Write-ColorOutput Yellow "Aviso: No se encuentra el directorio de build del frontend: $frontendBuildPath"
    }
}

# Paso 8: Invalidar caché de CloudFront (si es necesario)
if ($CLOUDFRONT_DOMAIN) {
    Write-ColorOutput Yellow "Paso 8: Invalidando caché de CloudFront..."
    try {
        $DISTRIBUTION_ID = (aws cloudfront list-distributions --query "DistributionList.Items[?DomainName=='$CLOUDFRONT_DOMAIN'].Id" --output text)
        if ($DISTRIBUTION_ID) {
            aws cloudfront create-invalidation --distribution-id $DISTRIBUTION_ID --paths "/*"
            Write-ColorOutput Green "Caché de CloudFront invalidada correctamente."
        }
        else {
            Write-ColorOutput Yellow "No se encontró la distribución de CloudFront para el dominio $CLOUDFRONT_DOMAIN"
        }
    }
    catch {
        Write-ColorOutput Yellow "No se pudo invalidar la caché de CloudFront: $_"
    }
}

Write-ColorOutput Green "¡Despliegue completado con éxito!"
if ($API_ENDPOINT) {
    Write-ColorOutput Green "URL de la API: $API_ENDPOINT"
}
if ($CLOUDFRONT_DOMAIN) {
    Write-ColorOutput Green "URL de la aplicación: https://$CLOUDFRONT_DOMAIN"
}
Write-ColorOutput Yellow "Si encuentras algún problema, verifica los logs en CloudWatch y el estado del stack en CloudFormation."