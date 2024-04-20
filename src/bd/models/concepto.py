from pydantic import BaseModel
from typing import Optional


class Concepto(BaseModel):
    id: Optional[str]
    #id: str | None
    codigo: Optional[str]
    descripcion: str
