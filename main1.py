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
from pydantic import BaseModel
#esto nos permite enviar una respuesta html al servidor 
from fastapi.responses import HTMLResponse

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/",tags=['Home'])
def read_root():
    return {"Hello": "World"}

# el parametro tiene que ir en llaves 
@app.get('/movies',tags=['Movies'])
def get_movies():
    #return HTMLResponse('<h1>Hola Luis</h1>')
    return movies 

@app.get('/movies/{id}',tags=['Movies'])
def get_movie(id:int):
    #return HTMLResponse('<h1>Hola Luis</h1>')
    #return id 
    #recorrer la lista y mostrar la que le id se parece 
    for movie in movies :
        if movie['id']==id:
            return movie      
    return []

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

#logica
#localhost:5000/movies/?id=123
@app.get('/movies/',tags=['Movies'])
def get_movie_by_category(category:str,year :int):
    #return category 
    for movie in movies :
        #comparamos el parametro con la query
        if movie['category']==category:
            return movie      
    return []

@app.post('/movies' , tags=['Movies'])
def create_movie(id:int=Body(),
                 title:str=Body(),
                 overview:str=Body(),
                 year:int=Body(),
                 rating:float =Body(),
                 category:str=Body()):
    movies.append({
        'id':id,
        'title':title,
        'overview':overview,
        'year':year,
        'rating':rating,
        'category':category
    })
    return movies 

@app.put('/movies/{id}',tags=['Movies'])
def update_movie(
                id:int,
                title:str=Body(),
                overview:str=Body(),
                year:int=Body(),
                rating:float =Body(),
                category:str=Body()   
):
    for movie in movies :
        if movie['id']==id:
            movie['title']=title
            movie['overview']=overview
            movie['year']=year
            movie['rating']=rating
            movie['category']=category
    return movies

@app.delete('/movies/{id}',tags=['Movies'])
def delete_movie(id:int):
    for movie in movies :
        if movie['id']==id:
            movies.remove(movie)
    return movies


    
