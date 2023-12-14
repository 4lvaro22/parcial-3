from fastapi import APIRouter, Request, Depends, Response, status, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from config.template import templates
from config.database import login_collection
from firebase_admin import auth
from services.dependencies import get_user_token
from schemas.log import logEntity
from datetime import datetime
import services.firebase

sso = APIRouter()

@sso.post("/signin", response_class=Jinja2Templates)
async def signin(request: Request, response: Response, token : str = Body()):
    try:
        decoded_token = auth.verify_id_token(token, clock_skew_seconds=10)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication from Firebase. {err}",
            headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
        )
    
    login_collection.insert_one({"timestamp": datetime.now(), "email": decoded_token["email"], "tokenId": token, "caducidad": datetime.fromtimestamp(decoded_token["exp"])})

    return templates.TemplateResponse("index.jinja", {"request": request})

@sso.get("/signout", response_class=Jinja2Templates)
async def signout(request: Request, res: Response, user = Depends(get_user_token)):
    auth.revoke_refresh_tokens(user['uid'])
    
    res = RedirectResponse(url='/', status_code=302)
    res.delete_cookie("token", path="/") 

    return res
