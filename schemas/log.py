from models.log_dto import Log
from models.filtrado_dto import Filtrado

def logList(loglist) -> list[Log]:
    return [logEntity(log) for log in loglist]

def logEntity(log) -> Log:
    return Log(**{
        **log})

def filtradoList(loglist) -> list[Filtrado]:
    return [filtradoEntity(log) for log in loglist]

def filtradoEntity(log) -> Log:
    return Filtrado(**{
        **log})