from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import cliente, fondos, transacciones
from app.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="API para gestión de fondos de inversión",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, esto debería limitarse a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas API
app.include_router(
    cliente.router,
    prefix=f"{settings.API_V1_PREFIX}/clientes",
    tags=["clientes"]
)
app.include_router(
    fondos.router,
    prefix=f"{settings.API_V1_PREFIX}/fondos",
    tags=["fondos"]
)
app.include_router(
    transacciones.router,
    prefix=f"{settings.API_V1_PREFIX}/transacciones",
    tags=["transacciones"]
)

@app.get("/", tags=["root"])
async def root():
    return {"message": "Bienvenido a la API de Fondos de EL CLIENTE"}