from fastapi import FastAPI 
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse,FileResponse,Response,JSONResponse
#importamos la ruta de movie
from src.routers.movie_router import movie_router
from src.utils.http_error_handler import HTTPErrorHandler

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()
#AQUI TRAEMOS EL MIDDLEWARE
app.add_middleware(HTTPErrorHandler)
#@app.middleware('http')
#async def http_error_handler(request:Request,call_next)->Response | JSONResponse:
   # print('Middleware is running!')
    #return await call_next(request)

static_path=os.path.join(os.path.dirname(__file__),'static/')
templates_path=os.path.join(os.path.dirname(__file__),'templates/')

app.mount('/static',StaticFiles(directory=static_path),'static')
templates =Jinja2Templates(directory=templates_path)

@app.get("/",tags=['Home'])
def home():
    #return PlainTextResponse(content='Home Luis',status_code=200)
    return templates.TemplateResponse('index.html')


@app.get('/get_file')
def get_file():
    return FileResponse('file.pdf')

app.include_router(prefix='/movies',router=movie_router)




    
