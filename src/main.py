from fastapi import FastAPI 
from fastapi.responses import PlainTextResponse,FileResponse
#importamos la ruta de movie
from src.routers.movie_router import movie_router
from src.utils.http_error_handler import HTTPErrorHandler
app = FastAPI()
#AQUI TRAEMOS EL MIDDLEWARE
app.add_middleware(HTTPErrorHandler)

@app.get("/",tags=['Home'])
def home():
    return PlainTextResponse(content='Home Luis',status_code=200)


@app.get('/get_file')
def get_file():
    return FileResponse('file.pdf')

app.include_router(prefix='/movies',router=movie_router)




    
