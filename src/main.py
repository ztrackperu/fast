from fastapi import FastAPI ,Depends
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse,FileResponse,Response,JSONResponse
#importamos la ruta de movie
from src.routers.movie_router import movie_router
from src.utils.http_error_handler import HTTPErrorHandler
from typing import Annotated
from src.routers.user_db import router_user

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from pymongo_get_database import get_database
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://192.168.1.185",
    "http://localhost:8000",
]
origins1 = ["*"]


#crear dependencias globales 
def dependency1():
    print("Global Dependeny1")

def dependency2():
    print("Global Dependeny2")

app = FastAPI(dependencies=[Depends(dependency1),Depends(dependency2)])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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

# responder un archivo den el directorio
@app.get('/get_file')
def get_file():
    return FileResponse('file.pdf')

app.include_router(prefix='/movies',router=movie_router)

app.include_router(prefix='/usersDb',router=router_user)


from pymongo_get_database import get_database
dbname = get_database()
 
# Recuperar una colección llamada "user_1_items" de la base de datos
cabeot = dbname["cabeot"]
dataot = dbname["dataot"]
 
def consulta(data:int):
    pipeline = [
        {"$project":{"_id":0,}},
        #{"$match": {"c_numot": 1000028211}},  
        {"$match": {"c_numot": data}}, 
        {
            "$lookup": {
                "from": 'detaot',
                "localField": 'c_numot',
                "foreignField": 'c_numot',
                "as": 'DetalleOt',
                "pipeline": [
                    {"$project":{"_id":0}} ,
                    {
                        "$lookup": {
                            "from": 'notmae',
                            "localField": 'c_numot',
                            "foreignField": 'c_NumOT',
                            "as": 'NotaSalida',
                            "pipeline": [
                                {"$project":{"_id":0}} ,
                                {
                                    "$lookup": {
                                        "from": 'notmov',
                                        "localField": 'NT_NDOC',
                                        "foreignField": 'NT_NDOC',
                                        "as": 'NotaSalidaDetalle',
                                        "pipeline": [
                                            {"$project":{"_id":0}},
                                            {
                                                "$lookup": {
                                                    "from": 'invmae',
                                                    "localField": 'NT_CART',
                                                    "foreignField": 'IN_CODI',
                                                    "as": 'DetalleInsumo',
                                                    "pipeline": [
                                                        {"$project":{"_id":0,"IN_ARTI":1,"IN_UVTA":1,"IN_COST":1}},                       
                                                    ]
                                                }
                                            }
                                        ]
                                    }
                                }
                            ],    
                        },
                    }
                ]
            }
        },   
    ]
    return pipeline

def consulta1(data:int):
    pipeline = [
        {"$project":{"_id":0,}},
        #{"$match": {"c_numot": 1000028211}},  
        {"$match": {"c_numot": data}},   
    ]
    return pipeline

def consulta2(data:int):
    pipeline = [
        {"$project":{"_id":0,}},
        {"$match": {"c_numot": data}},  
        {
            "$lookup": {
                "from": "detaot",
                "localField": "c_numot",
                "foreignField": "c_numot",
                "as": "DetalleOt",
                "pipeline": [
                    {"$project":{"_id":0}} ,
                ]
            },
        }, 
        {
            "$lookup": {
                "from": "notmae",
                "localField": "c_numot",
                "foreignField": "c_NumOT",
                "as":"NotaSalida",
                "pipeline": [
                    {"$project":{"_id":0}} ,
                    {
                        "$lookup": {
                            "from": 'notmov',
                            "localField": 'NT_NDOC',
                            "foreignField": 'NT_NDOC',
                            "as": 'NotaSalidaDetalle',
                            "pipeline": [
                                {"$project":{"_id":0}},
                                {
                                    "$lookup": {
                                        "from": 'detaoc',
                                        "localField": 'NT_CART',
                                        "foreignField": 'c_codprd',
                                        "as": 'detaoc',
                                        "pipeline": [
                                            {"$project":{"_id":0}},
                                            {"$sort" :{"c_numeoc":-1}} ,
                                            {"$limit" :1},
                                            {
                                                "$lookup": {
                                                    "from": 'invmae',
                                                    "localField": 'c_codprd',
                                                    "foreignField": 'IN_CODI',
                                                    "as": 'DetalleInsumo',
                                                    "pipeline": [
                                                        {"$project":{"_id":0,"IN_ARTI":1}},                                                                            
                                                    ]
                                                }
                                            },
                                            {
                                                "$lookup": {
                                                    "from": 'cabeoc',
                                                    "localField": 'c_numeoc',
                                                    "foreignField": 'c_numeoc',
                                                    "as": 'moneda',
                                                    "pipeline": [
                                                        {"$project":{"_id":0,"c_codmon":1}},                                                                           
                                                    ]
                                                }
                                        },
                                        ]
                                    }
            
                                }
                            ]
                        }
                    }
                ]
            }, 
        }
    ]
    return pipeline


#item_details = cabeot.aggregate(pipeline)
#item_details = cabeot.find().limit(1)
#print("olitas")
#print(item_details[0]->c_desequipo)
#for item in  item_details:
 # Esto no proporciona una salida muy legible
  #print("dentro")
  #print(item)

    
@app.get('/testOT2/{id}')
def get_ot(id:int):
    #item_details = cabeot.aggregate(consulta(id))
    item_details = dataot.aggregate(consulta1(id))
    for item in item_details :
        #return JSONResponse(content=item.model_dump(),status_code=200)
        return JSONResponse(content=dict(item),status_code=200)    

@app.get('/testOT/{id}')
def get_ot1(id:int):
    item_details = cabeot.aggregate(consulta(id))
    for item in item_details :
        #return JSONResponse(content=item.model_dump(),status_code=200)
        return JSONResponse(content=dict(item),status_code=200)     
    
@app.get('/testOT3/{id}')
def get_ot2(id:int,request :Request):
    item_details = cabeot.aggregate(consulta(id))
    for item in item_details :
        #return JSONResponse(content=item.model_dump(),status_code=200)
        #return JSONResponse(content=dict(item),status_code=200)  
        return templates.TemplateResponse('ot1.html',{ 'request':request,'message':item})
        #return datosOT(item)

@app.get('/testOT4/{id}')
def get_ot3(id:int,request :Request):
    item_details = cabeot.aggregate(consulta(id))
    for item in item_details :
        #return JSONResponse(content=item.model_dump(),status_code=200)
        #return JSONResponse(content=dict(item),status_code=200)  
        return templates.TemplateResponse('ot.html',{ 'request':request,'message':item})
        #return datosOT(item)

@app.get('/ot/{id}')
def get_ot4(id:int,request :Request):
    item_details = cabeot.aggregate(consulta2(id))
    for item in item_details :
      return JSONResponse(content=dict(item),status_code=200) 


