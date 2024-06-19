from passlib.context import CryptContext
import jwt
from dotenv import dotenv_values
from models import User
from fastapi.exceptions import HTTPException
from fastapi import status
config_cerdential = dotenv_values(".env")



pwd_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

def get_password_hash(password):
    return pwd_context.hash(password)
async def verfy_token (token:str):
    try:
        payload = jwt.decode(token,config_cerdential['SECRET'],algorithms=['HS256'])
        user = await User.get(id  = payload.get("id")) 
    except:
         raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED,
             detail= "invalide token",
             headers={"WWW.Authenticate":"Bearer"}
        
         )
    return user