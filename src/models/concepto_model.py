import datetime
from pydantic import BaseModel,Field,validator

class Concepto(BaseModel):
    id:int
    codigo:int
    descripcion:str
 

class ConceptoCreate(BaseModel):
    id:int
    codigo:int=Field(ge=1000)
    descripcion:str=Field(min_length=3,max_length=58)

    model_config = {
        'json_schema_extra':{
            'example':{
                'id':1,
                'codigo':1025,
                'descripcion':'descripcion del concepto la orden de trabajo ',
            }
        }
    }

