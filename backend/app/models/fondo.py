from pydantic import BaseModel


class Fondo(BaseModel):
    fundId: str
    name: str
    category: str  # FPV o FIC
    minimumAmount: float