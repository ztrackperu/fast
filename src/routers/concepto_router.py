from typing import List
from fastapi import Path,Query,APIRouter
from fastapi.responses import  JSONResponse
from src.models.concepto_model import Concepto ,ConceptoCreate
from pymongo_get_database import get_database
dbname = get_database()
conceptos_ot = dbname["conceptos_ot"]

concepto_router = APIRouter()

@concepto_router.get('/',tags=['ConceptoOT'])
def ListaConceptosOT():
    pip = [
        {"$match": {"estado": 1}},  
        {"$project":{"_id":0,}},
        {"$sort":{"descripcion":1}}        
    ]
    item_details = conceptos_ot.aggregate(pip)
    content1=[]
    for item in item_details :
        content1.append(item)
    return JSONResponse(content=content1,status_code=200)

@concepto_router.get('/{id}',tags=['ConceptoOT'])
def ListaConceptosOT1(id:int):
    pip = [
        {"$match": {"estado": 1,"codigo":id}},  
        {"$project":{"_id":0,}},       
    ]
    item_details = conceptos_ot.aggregate(pip)
    for item in item_details :
        return JSONResponse(content=item,status_code=200)  

@concepto_router.post('/' , tags=['ConceptoOT'])
def create_model(movie:ConceptoCreate):

    #movies.append(movie)
    #content = [movie.model_dump() for movie in movies]
    item_details = conceptos_ot.insertOne(movie)
    return JSONResponse(content=item_details,status_code=201)
