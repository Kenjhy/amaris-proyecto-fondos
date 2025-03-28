from fastapi import APIRouter, HTTPException
from typing import List
from app.models.fondo import Fondo
from app.services.fondo_service import FondoService

router = APIRouter()

@router.get("/", response_model=List[dict])
async def get_all_funds():
    """Obtiene todos los fondos disponibles"""
    return await FondoService.get_all_funds()

@router.get("/{fund_id}")
async def get_fund(fund_id: str):
    """Obtiene información de un fondo específico"""
    fund = await FondoService.get_fund(fund_id)
    if not fund:
        raise HTTPException(status_code=404, detail="Fondo no encontrado")
    return fund