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

#no debmso enviar directamente un diccionario como respuesta 
#debe ser una lista de objetos
#movies:List[Movie] =[]
#los parametros ruta son valores que podemos pasar por la url

from typing import Union
#validamos Parametro y queris 
from fastapi import FastAPI ,Body,Path,Query
from pydantic import BaseModel,Field
#esto nos permite enviar una respuesta html al servidor 
from fastapi.responses import HTMLResponse ,JSONResponse,PlainTextResponse,RedirectResponse,FileResponse
# para realizar esquemas importamos pydantic
from pydantic import BaseModel
#para usar opcional 
from typing import Optional,List
#importar manejador de fechas 
import datetime
# dependencias para validar parametros


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
    #id:int
    #title:str=Field(min_length=5,max_length=15,default="My Movie")
    #overview:str =Field(min_length=15,max_length=58,default="Esta pelicula trata acerca de ...")
    #año menor o igual al año actual y menor igual a 1900
    #year:int = Field(le=datetime.date.today().year,ge=1900 , default=2023)
    #rating:float =Field(ge=0,le=10, default=10)
    #category:str = Field(min_length=5,max_length=20,default="Acción")

    id:int
    title:str=Field(min_length=5,max_length=15)
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

movies:List[Movie] =[]

@app.get("/",tags=['Home'])
def home():
    #return {"Hello": "World"}
    return PlainTextResponse(content='Home Luis',status_code=200)

# el parametro tiene que ir en llaves 
@app.get('/movies',tags=['Movies'],status_code=200,response_description="Nos debe devolver una respuesta exitosa")
def get_movies()->List[Movie]:
    #return HTMLResponse('<h1>Hola Luis</h1>')
    #return movies 
    #return [movie.model_dump() for movie in movies]
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content,status_code=200)


@app.get('/movies/{id}',tags=['Movies'])
#hago una validacion con el path
#para validar que el id ingresado sea mayor a 0
def get_movie(id:int=Path(gt=0))->Movie | dict:
    #return HTMLResponse('<h1>Hola Luis</h1>')
    #return id 
    #recorrer la lista y mostrar la que le id se parece 
    for movie in movies :
        #if movie['id']==id:
        if movie.id==id:
            #return movie.model_dump()
            return JSONResponse(content=movie.model_dump(),status_code=200)      
    #return {}
    return JSONResponse(content={},status_code=404)      



@app.get('/movies/',tags=['Movies'])
def get_movie_by_category(category:str = Query(min_length=5,max_length=20))->Movie | dict:
    #return category 
    for movie in movies :
        #comparamos el parametro con la query
        #if movie['category']==category:
        if movie.category==category:
            #return movie.model_dump()      
    #return {}
            return JSONResponse(content=movie.model_dump(),status_code=200)      
    return JSONResponse(content={},status_code=404)    

@app.post('/movies' , tags=['Movies'])
def create_movie(movie:MovieCreate)->List[Movie]:
    #movies.append(movie.model_dump())
    movies.append(movie)
    #return movies 
    #return [movie.model_dump() for movie in movies]
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content,status_code=201)
    #303 es un aredireccion a nuestra propia aplicacion
    #return RedirectResponse('/movies',status_code=303)

@app.put('/movies/{id}',tags=['Movies'])
def update_movie(id:int,movie1:MovieUpdate)->List[Movie]:
    for movie in movies :
        if movie.id==id:
            movie.title=movie1.title
            movie.overview=movie1.overview
            movie.year=movie1.year
            movie.rating=movie1.rating
            movie.category=movie1.category
    #return movies
    #return [movie.model_dump() for movie in movies]
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content,status_code=200)


@app.delete('/movies/{id}',tags=['Movies'])
def delete_movie(id:int)->List[Movie]:
    for movie in movies :
        if movie.id==id:
            movies.remove(movie)
    #return movies
    #return [movie.model_dump() for movie in movies]
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content,status_code=200)

@app.get('/get_file')
def get_file():
    return FileResponse('file.pdf')



    
