from typing import Optional

from pydantic import BaseModel, EmailStr, Field, constr, conint


class SchemaDeSocie(BaseModel):
    nombre: constr(strict=True) = Field(...)
    apellido: constr(strict=True) = Field(...)
    dni: conint(strict=True) = Field(...)
    nro_socie: conint(strict=True, gt=0) = Field(...)
    email: EmailStr = Field(...)
    telefono: constr(strict=True) = Field()
    direccion: constr(strict=True) = Field()
    codigo_postal: constr(strict=True) = Field()
    tipo_socio: bool = Field()

    class config:
        schema_extra = {
            "ejemplo": {
                "nombre": "Juana",
                "apellido": "Pilo",
                "dni": 27358783,
                "nro_socie": 1234,
                "email": "jpilo@x.ar",
                "telefono": "+54 9 456789",
                "direccion": "calle pública S/n",
                "codigo_postal": "5823",
                "tipo_socio": True,
            }
        }


class UpdateSocieModel(BaseModel):
    nombre: Optional[constr(strict=True)]
    apellido: Optional[constr(strict=True)]
    dni: Optional[conint(strict=True)]
    nro_socie: Optional[conint(strict=True, gt=0)]
    email: Optional[EmailStr]
    telefono: Optional[constr(strict=True)]
    direccion: Optional[constr(strict=True)]
    codigo_postal: Optional[constr(strict=True)]
    tipo_socio: Optional[bool]

    class Config:
        schema_extra = {
            "ejemplo": {
                "nombre": "Juana",
                "apellido": "Pilo",
                "dni": 27358783,
                "nro_socie": 1234,
                "email": "jpilo@x.ar",
                "telefono": "+54 9 456789",
                "direccion": "calle pública S/n",
                "codigo_postal": "5823",
                "tipo_socio": True,
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}