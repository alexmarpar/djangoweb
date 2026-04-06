from fastapi import APIRouter, Depends, HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt,JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()



router = APIRouter(
    prefix="/jwtauth",
    tags=["jwtauth"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)




ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKE_DURATION = 1
SECRET_KEY = os.getenv("SECRET_KEY")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="jwtauth/login")

crypt = CryptContext(schemes=["argon2"])


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool


class UserDB(User):
    password: str


users_db = {"mario": {
            "username": "mario",
            "full_name": "alex mario",
            "email": "mario@example.com",
            "disable": False,
            "password": "$argon2i$v=19$m=16,t=2,p=1$eWJVZkZwTGRvazBXUVJsMg$LsuVSuR50Jp4v+ImtYytsw"
},
"luigi": {
            "username": "luigi",
            "full_name": "alex luigi",
            "email": "luigi@example.com",
            "disable": True,
            "password": "$argon2i$v=19$m=16,t=2,p=1$eWJVZkZwTGRvazBXUVJsMg$LsuVSuR50Jp4v+ImtYytsw"
    }
}
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
   
async def auth_user(token: str = Depends(oauth2_scheme)):
    
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas", headers={"WWW-authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
        

    except JWTError:
        raise exception
    
    return search_user(username)

async def current_user(user: User = Depends(auth_user)):
  
    if user.disable:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm= Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
   
    user = search_user_db(form.username)




    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
   


    access_token = {"sub":user.username, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKE_DURATION)}


    return {"access_token": jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM), "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user