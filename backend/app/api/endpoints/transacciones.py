from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.models.transaccion import TransaccionCreate
from app.services.transaccion_service import TransaccionService
from app.config import settings

router = APIRouter()

@router.post("/subscriptions")
async def create_subscription(
    subscription_data: TransaccionCreate, 
    client_id: str = settings.DEFAULT_CLIENT_ID
):
    """Suscribe al cliente a un fondo"""
    result = await TransaccionService.create_subscription(client_id, subscription_data)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.delete("/subscriptions/{fund_id}")
async def cancel_subscription(
    fund_id: str, 
    client_id: str = settings.DEFAULT_CLIENT_ID
):
    """Cancela la suscripción del cliente a un fondo"""
    result = await TransaccionService.cancel_subscription(client_id, fund_id)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/history")
async def get_transactions_history(
    client_id: str = settings.DEFAULT_CLIENT_ID,
    limit: int = Query(10, description="Número máximo de transacciones a devolver")
):
    """Obtiene el historial de transacciones del cliente"""
    return await TransaccionService.get_client_transactions(client_id, limit)

@router.get("/subscriptions")
async def get_active_subscriptions(client_id: str = settings.DEFAULT_CLIENT_ID):
    """Obtiene las suscripciones activas del cliente"""
    return await TransaccionService.get_client_active_subscriptions(client_id)