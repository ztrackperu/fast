from fastapi import FastAPI ,Depends
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse,FileResponse,Response,JSONResponse
#importamos la ruta de movie
from src.routers.movie_router import movie_router
from src.utils.http_error_handler import HTTPErrorHandler
from typing import Annotated

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
#crear dependencias globales 
def dependency1():
    print("Global Dependeny1")

def dependency2():
    print("Global Dependeny2")

app = FastAPI(dependencies=[Depends(dependency1),Depends(dependency2)])
#AQUI TRAEMOS EL MIDDLEWARE
app.add_middleware(HTTPErrorHandler)
#@app.middleware('http')
#async def http_error_handler(request:Request,call_next)->Response | JSONResponse:
   # print('Middleware is running!')
    #return await call_next(request)

static_path=os.path.join(os.path.dirname(__file__),'static/')
templates_path=os.path.join(os.path.dirname(__file__),'templates/')

app.mount('/static',StaticFiles(directory=static_path),'staticPablito')
templates =Jinja2Templates(directory=templates_path)

@app.get("/",tags=['Home'])
def home(request :Request):
    #return PlainTextResponse(content='Home Luis',status_code=200)
    return templates.TemplateResponse('index.html',{'request':request, 'message':'Welcome'})

# vamos hacer una funcion para evitar duplicidad de codigo con Dependencias
def common_params(start_date:str,end_date:str):
    return {"start_date":start_date,"end_date":end_date}

CommonDep =Annotated[dict,Depends(common_params)]

@app.get('/users')
def get_users(commons :CommonDep):
    return f"Users Created between {commons['start_date']} and {commons['end_date']}"

#otra froma de declarar dependencias 

class CommonDep1:
    def __init__(self,start_date:str,end_date:str) -> None:
        self.start_date =start_date
        self.end_date =end_date


@app.get('/customers')
#def get_customer(commons :dict =Depends(common_params)):
def get_customer(commons :CommonDep1= Depends(CommonDep1)):
    return f"Customers Created between {commons.start_date} and {commons.end_date}"

#@app.get('/users')
#def get_users(start_date:str,end_date:str):
    #return f"Users Created between {start_date} and {end_date}"

#@app.get('/customers')
#def get_customer(start_date:str,end_date:str):
    #return f"Customers Created between {start_date} and {end_date}"

@app.get('/get_file')
def get_file():
    return FileResponse('file.pdf')

app.include_router(prefix='/movies',router=movie_router)




    
