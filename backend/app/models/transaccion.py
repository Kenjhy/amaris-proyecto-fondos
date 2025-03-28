from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime
from uuid import uuid4


class Transaccion(BaseModel):
    transactionId: str = Field(default_factory=lambda: str(uuid4()))  # Toda transacción debe generar un identificador único.
    clientId: str
    fundId: str
    type: Literal["SUBSCRIPTION", "CANCELLATION"]
    amount: float
    transactionDate: datetime = Field(default_factory=datetime.now)
    status: Literal["COMPLETED", "FAILED"] = "COMPLETED"


class TransaccionCreate(BaseModel):
    fundId: str
    amount: Optional[float] = None  # Opcional, se calcula según el fondo


class Subscription(BaseModel):
    subscriptionId: str = Field(default_factory=lambda: str(uuid4()))
    clientId: str
    fundId: str
    amountSubscribed: float
    status: Literal["ACTIVE", "CANCELLED"] = "ACTIVE"
    subscriptionDate: datetime = Field(default_factory=datetime.now)