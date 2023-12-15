from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from config.template import templates
from config.database import login_collection, filtrado_collection
from services.dependencies import get_user_token
from schemas.log import logEntity, logList, filtradoEntity, filtradoList
from datetime import datetime
import pymongo

log = APIRouter()

PATH="/logs"

@log.get(PATH + "/login", response_class=Jinja2Templates)
async def show_login_logs(request: Request, user = Depends(get_user_token)):
    
    result_list = logList(login_collection.find().sort([("timestamp", pymongo.DESCENDING)]))

    for result in result_list:
        result.timestamp = result.timestamp.astimezone().isoformat()
        result.caducidad = result.caducidad.astimezone().isoformat()


    return templates.TemplateResponse("logs/logInicioSesion.jinja", {"request": request, "logs": result_list, "user": user})


@log.get(PATH + "/filtrado", response_class=Jinja2Templates)
async def show_filtrado_logs(request: Request, user = Depends(get_user_token)):

    result_list = filtradoList(filtrado_collection.find().sort([("timestamp", pymongo.DESCENDING)]))

    for result in result_list:
        result.timestamp = result.timestamp.astimezone().isoformat()

    return templates.TemplateResponse("logs/logFiltrado.jinja", {"request": request, "logs": result_list, "user": user})
