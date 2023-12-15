from cloudinary.uploader import upload_image
from fastapi import APIRouter, HTTPException, UploadFile, status
import config.cloudinary 
from uuid import uuid4

def setImage(entity : dict, image : UploadFile, key : str = "images",):
    imagesUrl = ""

    if image.size > 0 and image.content_type.startswith("image"):
        response = upload(image, folder="parcial-3")
        imagesUrl = response
    if imagesUrl != "":
        entity[key] = imagesUrl

def upload(file, folder=""):
    if file is None:
            raise HTTPException(status_code=400, detail="Bad Request")
            
    public_id = uuid4()

    file.filename = str(public_id)
    
    response = upload_image(file.file, folder)
    
    if response is None:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return response.build_url()