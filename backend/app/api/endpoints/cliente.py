from fastapi import APIRouter, HTTPException
from app.models.cliente import Cliente, ClienteUpdate
from app.services.cliente_service import ClienteService
from app.config import settings

router = APIRouter()

@router.get("/{client_id}")
async def get_client(client_id: str = settings.DEFAULT_CLIENT_ID):
    """Obtiene información del cliente"""
    client = await ClienteService.get_client(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return client

@router.patch("/{client_id}")
async def update_client(client_id: str, client_data: ClienteUpdate):
    """Actualiza preferencias del cliente"""
    updated = await ClienteService.update_client_preferences(client_id, client_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Cliente no encontrado o error al actualizar")
    return updated