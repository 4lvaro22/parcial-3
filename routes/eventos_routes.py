from fastapi import APIRouter, Request, UploadFile, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from config.database import eventos_collection
from schemas.entity import eventosList, eventosEntity
from datetime import datetime
from bson import ObjectId
from config.template import templates
from services.dependencies import get_user_token, get_user_token_ignore, formdata_to_json
from services.cloudinary import setImage
from pydantic import Field
import pymongo

eventos = APIRouter()

@eventos.get("/", response_class=Jinja2Templates)
async def main(request: Request, user = Depends(get_user_token_ignore)):
    return templates.TemplateResponse("index.jinja", {"request": request, "entities_list": [], "user": user})

@eventos.post("/", response_class=Jinja2Templates)
async def main(request: Request, user = Depends(get_user_token_ignore)):
    formdata = await request.form()
    json_data = formdata_to_json(formdata)
    
    if json_data != {} and json_data["ubicacion"] != '':
        result_list = eventosList(eventos_collection.find().sort("timestamp", pymongo.ASCENDING))
        result_list = [result for result in result_list if abs(result.latitud - float(json_data["lat"])) <= 0.2 and abs(result.longitud - float(json_data["lon"])) <= 0.2]
    else:
        result_list = []

    lugares = [lugar.lugar for lugar in result_list]

    return templates.TemplateResponse("index.jinja", {"request": request, "entities_list": result_list, "user": user, "lugares": lugares, "principal": json_data["ubicacion"]})

@eventos.get("/mostrar/{id}", response_class=Jinja2Templates)
async def show_entity(request: Request, id: str, user = Depends(get_user_token_ignore)):
    result_list = eventosEntity(eventos_collection.find_one({"_id": ObjectId(id)}))

    return templates.TemplateResponse("mostrarEntidad.jinja", {"request": request, "entity": result_list, "user": user})

@eventos.get("/crear", response_class=Jinja2Templates)
async def create_entity(request: Request, user = Depends(get_user_token)):
    return templates.TemplateResponse("crearEntidad.jinja", {"request": request, "user": user})

@eventos.post("/crear", response_class=RedirectResponse)
async def create_entity(request: Request, file: UploadFile = None, user = Depends(get_user_token)): 
    formdata = await request.form()
    json_data = formdata_to_json(formdata)

    setImage(json_data, image=file)
    json_data["organizador"] = user["firebase"]["identities"]["email"][0]
    json_data["timestamp"] = datetime.strptime(json_data["timestamp"],'%Y-%m-%dT%H:%M')


    eventos_collection.insert_one(json_data)

    return RedirectResponse("/", status_code=302)

@eventos.get("/editar/{id}", response_class=Jinja2Templates)
async def update_entity(request: Request, id: str, user = Depends(get_user_token)):

    result = eventos_collection.find_one({"_id": ObjectId(id)})

    if user["email"] != result["organizador"]:
        return templates.TemplateResponse("error/error-403.jinja", {"request": request, "user": user})

    return templates.TemplateResponse("editarEntidad.jinja", {"request": request, "entity": result, "user": user})

@eventos.post("/editar/{id}", response_class=Jinja2Templates)
async def update_entity(request: Request, id: str, file: UploadFile = None, user = Depends(get_user_token)): 

    formdata = await request.form()
    json_data = formdata_to_json(formdata)

    if file.size > 0:
        setImage(json_data, image=file)
    if(json_data["timestamp"] != ''):
        json_data["timestamp"] = datetime.strptime(json_data["timestamp"],'%Y-%m-%dT%H:%M')
    else:
        del json_data["timestamp"]

    eventos_collection.update_one({"_id": ObjectId(id)}, {"$set": {**json_data}})

    return RedirectResponse("/", status_code=302)

@eventos.get("/borrar/{id}", response_class=Jinja2Templates)
async def delete_entity(request: Request, id: str, user = Depends(get_user_token)):  
    result = eventos_collection.find_one({"_id": ObjectId(id)})

    if user["email"] != result["organizador"]:
        return templates.TemplateResponse("error-403.jinja", {"request": request, "user": user})
    
    eventos_collection.delete_one({"_id": ObjectId(id)})

    return RedirectResponse("/", status_code=302)