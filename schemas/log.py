from models.log_dto import Log

def logList(loglist) -> list[Log]:
    return [logEntity(log) for log in loglist]

def logEntity(log) -> Log:
    return Log(**{
        **log})