from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import uuid4


class Cliente(BaseModel):
    clientId: str = Field(default_factory=lambda: str(uuid4()))
    balance: float = 500000.0  # Se posee un monto inicial de COP $500.000.
    preferredNotification: str = "email"  # Por defecto email
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class ClienteUpdate(BaseModel):
    preferredNotification: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None