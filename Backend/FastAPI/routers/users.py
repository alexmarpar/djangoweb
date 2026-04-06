from fastapi import APIRouter, HTTPException
from pydantic import BaseModel 


router = APIRouter(
    #docs_url=None,
    #redoc_url=None
)

# Inicia el server: uvicorn main:app --reload

# Entidad user
class User(BaseModel):
    id: int
    name: str
    sourname: str
    url: str
    age: int

Users_list=[User(id = 1, name = "Mario",sourname= "mario",url = "https://mario.com", age = 35),
            User(id = 2,name = "luigi", sourname = "dev", url = "https://luigi.com", age = 36),
            User(id = 3,name = "Mario",sourname = "galaxy",url = "https://mario.com", age = 44)]


@router.get("/usersjson")
async def usersjson():
    return [{"name": "Brais", "sourname": "moure","url": "https://moure.dev", "age": 35},
            {"name": "Moure", "sourname": "dev","url": "https://moure.com", "age": 35},
            {"name": "Mario", "sourname": "galaxy","url": "https://mario.com", "age": 44}]

@router.get("/users")
async def users():
    return Users_list

#Path
@router.get("/user/{id}")
async def user(id: int):
    users = filter(lambda user: user.id==id, Users_list)
    try:
        return list(users)[0]
    except:
        return {"Error": "No se ha encontrado el usuario"}
    
#Query

@router.get("/userquery/")
async def user(id: int):
    return search_user(id)
    
# Post
@router.post("/user/", response_model=user, status_code=201)
async def user(user: User):
    if type(search_user(user.id))==User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    
    Users_list.append(user)
    return user

# Put
@router.put("/user/")
async def user(user: User):
    found = False

    for index, saved_user in enumerate(Users_list):
        if saved_user.id == user.id:
            Users_list[index] = user
            found=True
    
    if not found:
        return {"Error": "Usuario no se ha actualizado el usuario "}
    
    return user

# Delete

@router.delete("/user/{id}")
async def user(id: int):
    found = False

    for index, saved_user in enumerate(Users_list):
        if saved_user.id == id:
            Users_list[index] = user
            del Users_list[index]
            found = True
    
    if not found:
        return {"Error": "Usuario no se ha eliminado el usuario "}


def search_user(id: int):
    users = filter(lambda user: user.id==id, Users_list)
    try:
        return list(users)[0]
    except:
        return {"Error": "No se ha encontrado el usuario"}
    
# Códigos HTTP: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status
# Códigos HTTP Documentación FastAPI: https://fastapi.tiangolo.com/es/tutorial/handling-errors/