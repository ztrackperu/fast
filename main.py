#from fastapi import FastAPI

#app = FastAPI()

#app.title = "Mi primera aplicacion con FastAPI"
#app.version ="2.0"
#@app.get('/',tags=['Home'])

#def home():
    #return "Hola mundo luis!"
#@app.get('/home',tags=['Home'])

#def home():
    #return "Hola mundo luis!"
movies =[
    {
        "id":1,
        "title": "Avatar",
        "overview" : "En el exuberante planeta llamado Pandora ...",
        "year":"2009",
        "rating":7.8,
        "category":"Aventura"
    },
    {
        "id":2,
        "title": "Avatar 2",
        "overview" : "En el exuberante planeta llamado Pandora ...",
        "year":"2009",
        "rating":7.8,
        "category":"Acción"
    }
]
#los parametros ruta son valores que podemos pasar por la url

from typing import Union

from fastapi import FastAPI ,Body
from pydantic import BaseModel,Field
#esto nos permite enviar una respuesta html al servidor 
from fastapi.responses import HTMLResponse
# para realizar esquemas importamos pydantic
from pydantic import BaseModel
#para usar opcional 
from typing import Optional,List
#importar manejador de fechas 
import datetime

app = FastAPI()

class Movie(BaseModel):
    #sin Optional
    #id:int | None =None
    #con Optional
    #id:Optional[int]=None
    #modelo usado solo pa registar y listar
    id:int
    title:str
    overview:str
    year:int
    rating:float 
    category:str

class MovieCreate(BaseModel):
    id:int
    title:str=Field(min_length=5,max_length=15)
    overview:str =Field(min_length=15,max_length=58)
    #año menor o igual al año actual y menor igual a 1900
    year:int = Field(le=datetime.date.today().year,ge=1900)
    rating:float 
    category:str

#para validar numeros 

class MovieUpdate(BaseModel):
    #modelo pa actualizar
    title:str
    overview:str
    year:int
    rating:float 
    category:str

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/",tags=['Home'])
def read_root():
    return {"Hello": "World"}

# el parametro tiene que ir en llaves 
@app.get('/movies',tags=['Movies'])
def get_movies()->List[Movie]:
    #return HTMLResponse('<h1>Hola Luis</h1>')
    return movies 

@app.get('/movies/{id}',tags=['Movies'])
def get_movie(id:int)->Movie:
    #return HTMLResponse('<h1>Hola Luis</h1>')
    #return id 
    #recorrer la lista y mostrar la que le id se parece 
    for movie in movies :
        if movie['id']==id:
            return movie      
    return []


@app.get('/movies/',tags=['Movies'])
def get_movie_by_category(category:str,year :int)->Movie:
    #return category 
    for movie in movies :
        #comparamos el parametro con la query
        if movie['category']==category:
            return movie      
    return []

@app.post('/movies' , tags=['Movies'])
def create_movie(movie:MovieCreate)->List[Movie]:
    movies.append(movie.model_dump())
    return movies 

@app.put('/movies/{id}',tags=['Movies'])
def update_movie(id:int,movie1:MovieUpdate)->List[Movie]:
    for movie in movies :
        if movie['id']==id:
            movie['title']=movie1.title
            movie['overview']=movie1.overview
            movie['year']=movie1.year
            movie['rating']=movie1.rating
            movie['category']=movie1.category
    return movies

@app.delete('/movies/{id}',tags=['Movies'])
def delete_movie(id:int)->List[Movie]:
    for movie in movies :
        if movie['id']==id:
            movies.remove(movie)
    return movies


    
