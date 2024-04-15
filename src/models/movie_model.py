import datetime
from pydantic import BaseModel,Field,validator

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