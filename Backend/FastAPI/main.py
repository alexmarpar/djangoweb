from fastapi import FastAPI 
from routers import products,users,jwt_auth_users,basic_auth_users,users_db
from fastapi.staticfiles import StaticFiles


app = FastAPI(
    #docs_url=None, // You can use https://<<example_url>>/docs or https://<<example_url>>/redoc to consult the  requests methods avaliable 
    #redoc_url=None
)
# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)
app.include_router(users_db.router)
app.mount("/static",StaticFiles(directory="static"), name="static")




@app.get("/")
async def root():
    return "¡Hola FastAPI"  # Asincrono    // segundo plano

@app.get("/url")
async def url():
    return {"url_curso": "https://mouredev.com/python"}

# Ejercicio tags y ordenar pendiente de hacer
# Cookies: https://fastapi.tiangolo.com/es/tutorial/cookie-params/
