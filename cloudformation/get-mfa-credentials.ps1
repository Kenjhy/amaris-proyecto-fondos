# Script para obtener credenciales temporales con MFA
param (
    [Parameter(Mandatory=$true)]
    [string]$MfaSerialNumber,
    
    [Parameter(Mandatory=$true)]
    [string]$TokenCode,
    
    [Parameter(Mandatory=$false)]
    [int]$DurationSeconds = 43200  # 12 horas
)

Write-Host "Obteniendo credenciales temporales con MFA..." -ForegroundColor Yellow

try {
    # Obtener credenciales temporales
    $credentials = aws sts get-session-token `
        --serial-number $MfaSerialNumber `
        --token-code $TokenCode `
        --duration-seconds $DurationSeconds `
        --output json | ConvertFrom-Json
    
    # Verificar si se obtuvieron las credenciales
    if (-not $credentials -or -not $credentials.Credentials) {
        throw "No se pudieron obtener las credenciales"
    }
    
    # Mostrar las credenciales
    Write-Host "Credenciales obtenidas correctamente." -ForegroundColor Green
    Write-Host ""
    Write-Host "Exporta estas variables de entorno para usar las credenciales:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Para PowerShell:" -ForegroundColor Cyan
    Write-Host "`$env:AWS_ACCESS_KEY_ID = '$($credentials.Credentials.AccessKeyId)'"
    Write-Host "`$env:AWS_SECRET_ACCESS_KEY = '$($credentials.Credentials.SecretAccessKey)'"
    Write-Host "`$env:AWS_SESSION_TOKEN = '$($credentials.Credentials.SessionToken)'"
    Write-Host ""
    Write-Host "Para CMD:" -ForegroundColor Cyan
    Write-Host "set AWS_ACCESS_KEY_ID=$($credentials.Credentials.AccessKeyId)"
    Write-Host "set AWS_SECRET_ACCESS_KEY=$($credentials.Credentials.SecretAccessKey)"
    Write-Host "set AWS_SESSION_TOKEN=$($credentials.Credentials.SessionToken)"
    Write-Host ""
    Write-Host "Expiran el: $($credentials.Credentials.Expiration)" -ForegroundColor Yellow
    
    # Opcionalmente, configurar automáticamente para la sesión actual de PowerShell
    $setNow = Read-Host "¿Deseas configurar estas credenciales para esta sesión de PowerShell? (s/n)"
    if ($setNow -eq "s") {
        $env:AWS_ACCESS_KEY_ID = $credentials.Credentials.AccessKeyId
        $env:AWS_SECRET_ACCESS_KEY = $credentials.Credentials.SecretAccessKey
        $env:AWS_SESSION_TOKEN = $credentials.Credentials.SessionToken
        Write-Host "Credenciales configuradas para esta sesión." -ForegroundColor Green
    }
    
} catch {
    Write-Host "Error al obtener credenciales: $_" -ForegroundColor Red
    exit 1
}