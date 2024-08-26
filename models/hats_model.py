from pydantic import BaseModel
from typing import List, Optional

class HatUpdate(BaseModel):
    nome_chapeu: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    tamanho: Optional[str] = None
    cores_disponiveis: Optional[List[str]] = None
    disponivel: Optional[bool] = None

    class Config:
        orm_mode = True

class Hat(BaseModel):
    hat_id: int  
    nome_chapeu: str
    descricao: str
    preco: float
    tamanho: str
    cores_disponiveis: List[str]
    collection_id: int 
    disponivel: bool
    data_criacao: str

    class Config:
        orm_mode = True


class HatCreate(BaseModel):
    nome_chapeu: str
    preco: float
    tamanho: str
    cores_disponiveis: List[str]

    descricao: Optional[str] = None
    collection_id: Optional[int] = None
    disponivel: Optional[bool] = True
