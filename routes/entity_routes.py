from fastapi import APIRouter, Request, UploadFile, Depends, status, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from config.database import entity_collection
from schemas.entity import entityList
from datetime import datetime
from bson import ObjectId
from config.template import templates
from services.dependencies import get_user_token, get_user_token_ignore, formdata_to_json
from services.cloudinary import setImage

entity = APIRouter()

@entity.get("/", response_class=Jinja2Templates)
async def main(request: Request, user = Depends(get_user_token_ignore)):

    result_list = entityList(entity_collection.find())

    return templates.TemplateResponse("index.jinja", {"request": request, "entities_list": result_list, "user": user})

@entity.get("/mostrar", response_class=Jinja2Templates)
async def show_entity(request: Request, user = Depends(get_user_token)):

    result_list = entityList(entity_collection.find())

    if result_list == []:
        return templates.TemplateResponse("sinDatos.jinja", {"request": request, "user": user})
    else:
        return templates.TemplateResponse("mostrarEntidad.jinja", {"request": request, "entities_list": result_list, "user": user})

@entity.get("/mostrar/{email}", response_class=Jinja2Templates)
async def show_entity(request: Request, user = Depends(get_user_token), email:str = None):

    result_list = entityList(entity_collection.find({"email": email}))

    if result_list == []:
        return templates.TemplateResponse("sinDatos.jinja", {"request": request, "user": user})
    else:
        return templates.TemplateResponse("mostrarEntidad.jinja", {"request": request, "entities_list": result_list, "user": user})

@entity.get("/mostrar", response_class=Jinja2Templates)
async def show_entity(request: Request, user = Depends(get_user_token)):

    result_list = entityList(entity_collection.find())
    
    return templates.TemplateResponse("mostrarEntidad.jinja", {"request": request, "entities_list": result_list, "user": user})

@entity.get("/crear", response_class=Jinja2Templates)
async def create_entity(request: Request, user = Depends(get_user_token)):
    return templates.TemplateResponse("crearEntidad.jinja", {"request": request, "user": user})

@entity.post("/crear", response_class=RedirectResponse)
async def create_entity(request: Request, file: UploadFile = None, user = Depends(get_user_token)): # list[UploadFile] = []):
    
    # cloudinary_response = []
    # for file in file:
    #     cloudinary_response.append(cloudinary.uploader.upload(file.file, folder="parcial-3")["url"])
    formdata = await request.form()
    json_data = formdata_to_json(formdata)

    setImage(json_data, image=file)

    json_data["created_at"] = datetime.now()
    json_data["updated_at"] = datetime.now()
    json_data["email"] = user["firebase"]["identities"]["email"][0]
    json_data["userphoto"] = user["picture"]
    json_data["username"] = user["name"]
    entity_collection.insert_one(json_data)

    return RedirectResponse("/", status_code=302)

@entity.get("/editar/{id}", response_class=Jinja2Templates)
async def update_entity(request: Request, id: str, user = Depends(get_user_token)):

    result = entity_collection.find_one({"_id": ObjectId(id)})

    if user.email != result["email"]:
        return templates.TemplateResponse("error-403.jinja", {"request": request, "user": user})

    return templates.TemplateResponse("editarEntidad.jinja", {"request": request, "entity": result, "user": user})

@entity.post("/editar/{id}", response_class=Jinja2Templates)
async def update_entity(request: Request, id: str, file: UploadFile = None, user = Depends(get_user_token)): 

    formdata = await request.form()
    json_data = formdata_to_json(formdata)

    if file.size > 0:
        setImage(json_data, image=file)

    json_data["updated_at"] = datetime.now()

    entity_collection.update_one({"_id": ObjectId(id)}, {"$set": {**json_data}})

    return RedirectResponse("/", status_code=302)

@entity.get("/borrar/{id}", response_class=Jinja2Templates)
async def delete_entity(request: Request, id: str, user = Depends(get_user_token)):  
    result = entity_collection.find_one({"_id": ObjectId(id)})

    if user.email != result["email"]:
        return templates.TemplateResponse("error-403.jinja", {"request": request, "user": user})
    
    entity_collection.delete_one({"_id": ObjectId(id)})

    return templates.TemplateResponse("index.jinja", {"request": request, "user": user})