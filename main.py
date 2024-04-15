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

from fastapi import FastAPI
from pydantic import BaseModel
#esto nos permite enviar una respuesta html al servidor 
from fastapi.responses import HTMLResponse

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}

# el parametro tiene que ir en llaves 
@app.get('/movies',tags=['Home'])
def get_movies():
    #return HTMLResponse('<h1>Hola Luis</h1>')
    return movies 

@app.get('/movies/{id}',tags=['Home'])
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
@app.get('/movies/',tags=['Home'])
def get_movie_by_category(category:str,year :int):
    #return category 
    for movie in movies :
        #comparamos el parametro con la query
        if movie['category']==category:
            return movie      
    return []