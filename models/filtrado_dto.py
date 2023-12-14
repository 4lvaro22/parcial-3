from pydantic import BaseModel
from datetime import datetime

class Filtrado(BaseModel):
    timestamp: datetime
    email: str
    accion: str