from fastapi import APIRouter, HTTPException,status
from pydantic import BaseModel 
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema,users_schema
from bson import ObjectId


router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

# Inicia el server: uvicorn main:app --reload

# Entidad user

Users_list=[]


@router.get("/",response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

#Path
@router.get("/{id}")
async def user(id: str):
        return search_user("_id", ObjectId(id))
    
#Query

@router.get("/")
async def user(id: str):
    return search_user("_id", ObjectId(id))

# Post
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email))==User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    user_dict = dict(user)
    del user_dict["id"]
    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id": id}))

    return User(**new_user)

# Put
@router.put("/",  response_model=User)
async def user(user: User):
    user_dict = dict(user)
    del user_dict["id"]
    try:
        
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)

    except:
        return {"Error": "Usuario no se ha actualizado el usuario "}
    
    return search_user("_id", ObjectId(user.id))

# Delete

@router.delete("/{id}")
async def user(id: str, status_code=status.HTTP_204_NO_CONTENT):

    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    
    if not found:
        return {"Error": "Usuario no se ha eliminado el usuario "}


def search_user(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"Error": "No se ha encontrado el usuario"}
    
# Códigos HTTP: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status
# Códigos HTTP Documentación FastAPI: https://fastapi.tiangolo.com/es/tutorial/handling-errors/