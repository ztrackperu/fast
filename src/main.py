
from typing import Union
#validamos Parametro y queris 
from fastapi import FastAPI ,Body,Path,Query
#manejo de errores personalizados 
from pydantic import BaseModel,Field,validator
from fastapi.responses import HTMLResponse ,JSONResponse,PlainTextResponse,RedirectResponse,FileResponse
from typing import Optional,List
#importamos la ruta de movie
from src.routers.movie_router import movie_router
import datetime

app = FastAPI()

app.include_router(router=movie_router)

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None



@app.get("/",tags=['Home'])
def home():
    #return {"Hello": "World"}
    return PlainTextResponse(content='Home Luis',status_code=200)



@app.get('/get_file')
def get_file():
    return FileResponse('file.pdf')



    
