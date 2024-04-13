from fastapi import FastAPI

app = FastAPI()

app.title = "Mi primera aplicacion con FastAPI"
app.version ="2.0"
@app.get('/',tags=['Home'])

def home():
    return "Hola mundo luis!"
@app.get('/home',tags=['Home'])

def home():
    return "Hola mundo luis!"