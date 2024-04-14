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
        "category":"Acción"
    }
]

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


@app.get('/movies',tags=['Home'])
def home():
    #return HTMLResponse('<h1>Hola Luis</h1>')
    return movies 

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}