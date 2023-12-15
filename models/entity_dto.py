from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class Eventos (BaseModel):
    id: str
    name: str
    timestamp: datetime
    images: str
    latitud: float
    longitud: float
    lugar: str
    organizador:str
