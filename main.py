

from typing import Union
#validamos Parametro y queris 
from fastapi import FastAPI ,Body,Path,Query
#manejo de errores personalizados 
from pydantic import BaseModel,Field,validator
#esto nos permite enviar una respuesta html al servidor 
from fastapi.responses import HTMLResponse ,JSONResponse,PlainTextResponse,RedirectResponse,FileResponse
#para usar opcional 
from typing import Optional,List
#importar manejador de fechas 
import datetime

app = FastAPI()

class Movie(BaseModel):
    id:int
    title:str
    overview:str
    year:int
    rating:float 
    category:str

class MovieCreate(BaseModel):

    id:int
    title:str
    overview:str =Field(min_length=15,max_length=58)
    #año menor o igual al año actual y menor igual a 1900
    year:int = Field(le=datetime.date.today().year,ge=1900 )
    rating:float =Field(ge=0,le=10)
    category:str = Field(min_length=5,max_length=20)

    model_config = {
        'json_schema_extra':{
            'example':{
                'id':1,
                'title':'My movie',
                'overview':'Esta pelicula trata acerca de ...',
                'year': 2022,
                'rating':5,
                'category':'Comedia'
            }
        }
    }
    @validator('title')
    def validate_title(cls,value):
        if len(value)<5:
            raise ValueError('Title field must have a minium length of 5 charecters Luis')
        if len(value)>15:
            raise ValueError('Title field must have a maximun length of 15 charecters Luis')
        return value

class MovieUpdate(BaseModel):
    title:str
    overview:str
    year:int
    rating:float 
    category:str

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

movies:List[Movie] =[]

@app.get("/",tags=['Home'])
def home():
    #return {"Hello": "World"}
    return PlainTextResponse(content='Home Luis',status_code=200)

# el parametro tiene que ir en llaves 
@app.get('/movies',tags=['Movies'],status_code=200,response_description="Nos debe devolver una respuesta exitosa")
def get_movies()->List[Movie]:
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content,status_code=200)


@app.get('/movies/{id}',tags=['Movies'])
def get_movie(id:int=Path(gt=0))->Movie | dict: 
    for movie in movies :
        if movie.id==id:
            return JSONResponse(content=movie.model_dump(),status_code=200)      
    return JSONResponse(content={},status_code=404)      



@app.get('/movies/',tags=['Movies'])
def get_movie_by_category(category:str = Query(min_length=5,max_length=20))->Movie | dict:
    for movie in movies :
        if movie.category==category:
            return JSONResponse(content=movie.model_dump(),status_code=200)      
    return JSONResponse(content={},status_code=404)    

@app.post('/movies' , tags=['Movies'])
def create_movie(movie:MovieCreate)->List[Movie]:
    movies.append(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content,status_code=201)

@app.put('/movies/{id}',tags=['Movies'])
def update_movie(id:int,movie1:MovieUpdate)->List[Movie]:
    for movie in movies :
        if movie.id==id:
            movie.title=movie1.title
            movie.overview=movie1.overview
            movie.year=movie1.year
            movie.rating=movie1.rating
            movie.category=movie1.category
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content,status_code=200)


@app.delete('/movies/{id}',tags=['Movies'])
def delete_movie(id:int)->List[Movie]:
    for movie in movies :
        if movie.id==id:
            movies.remove(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content,status_code=200)

@app.get('/get_file')
def get_file():
    return FileResponse('file.pdf')



    
