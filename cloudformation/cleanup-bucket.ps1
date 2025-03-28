# Script para limpiar un bucket de S3 que está bloqueando la eliminación de un stack
# Este script vacía el bucket para que pueda ser eliminado por CloudFormation

param (
    [string]$BucketName = "elcliente-frontend-891377403177-prod"
)

Write-Host "Vacíando el bucket $BucketName..." -ForegroundColor Yellow

# Vaciar todos los objetos del bucket
Write-Host "Eliminando todos los objetos..."
aws s3 rm s3://$BucketName --recursive

# Eliminar todas las versiones de objetos si está habilitado el versionamiento
Write-Host "Comprobando si el bucket tiene versionamiento..."
$versioning = aws s3api get-bucket-versioning --bucket $BucketName | ConvertFrom-Json

if ($versioning.Status -eq "Enabled" -or $versioning.Status -eq "Suspended") {
    Write-Host "Eliminando todas las versiones de objetos..."
    $versions = aws s3api list-object-versions --bucket $BucketName | ConvertFrom-Json
    
    # Eliminar versiones
    if ($versions.Versions -and $versions.Versions.Count -gt 0) {
        foreach ($version in $versions.Versions) {
            Write-Host "Eliminando $($version.Key) versión $($version.VersionId)"
            aws s3api delete-object --bucket $BucketName --key $version.Key --version-id $version.VersionId
        }
    }
    
    # Eliminar marcadores de eliminación
    if ($versions.DeleteMarkers -and $versions.DeleteMarkers.Count -gt 0) {
        foreach ($marker in $versions.DeleteMarkers) {
            Write-Host "Eliminando marcador de eliminación $($marker.Key) versión $($marker.VersionId)"
            aws s3api delete-object --bucket $BucketName --key $marker.Key --version-id $marker.VersionId
        }
    }
}

Write-Host "Bucket $BucketName vacíado correctamente." -ForegroundColor Green
Write-Host "Ahora puedes intentar eliminar el stack de nuevo." -ForegroundColor Green