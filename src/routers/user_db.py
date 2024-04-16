# Clase en vídeo: https://youtu.be/_y9qQZXE24A?t=20480

### Users DB API ###

from fastapi import APIRouter, HTTPException, status
from src.bd.models.user import User
from src.bd.schemas.user import user_schema, users_schema 
from src.bd.client import db_client
from bson import ObjectId

#router_user = APIRouter(prefix="/userdb",
                   #tags=["userdb"],
                   #responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

router_user = APIRouter()

@router_user.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())


@router_user.get("/{id}")  # Path
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router_user.get("/")  # Query
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router_user.post("/", tags=['usersDB'] ,response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    #Mi entidad trasfromado en diccionario 
    user_dict = dict(user)
    #elimino el campo id 
    del user_dict["id"]
    #insersion en base de datos y captura del id insertardo
    id = db_client.monTest.users.insert_one(user_dict).inserted_id
    #buscar el id e insertar dat
    # user_schema es la estructura del json que esta en carpeta schema
    new_user = user_schema(db_client.monTest.users.find_one({"_id": id}))
    #realizamos la trasformacion de la base de datos al modelo User
    return User(**new_user)


@router_user.put("/", response_model=User)
async def user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error": "No se ha actualizado el usuario"}

    return search_user("_id", ObjectId(user.id))


@router_user.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):

    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"error": "No se ha eliminado el usuario"}

# Helper


def search_user(field: str, key):

    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}
