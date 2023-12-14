from pydantic import BaseModel
from datetime import datetime

class Log(BaseModel):
    timestamp: datetime
    email: str
    caducidad: datetime
    tokenId: str