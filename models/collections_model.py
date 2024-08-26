from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CollectionUpdate(BaseModel):
    nome_colecao: Optional[str] = None
    descricao: Optional[str] = None
    disponivel: Optional[bool] = None

    class Config:
        orm_mode = True

class CollectionCreate(BaseModel):
    nome_colecao: str
    descricao: Optional[str] = None
    disponivel: bool = False

class Collection(BaseModel):
    collection_id: int
    nome_colecao: str
    descricao: Optional[str]
    data_criacao: datetime
    disponivel: bool = False

    class Config:
        populate_by_name = True
        from_attributes = True
        arbitrary_types_allowed = True