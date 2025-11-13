from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class Utenti(BaseModel):
    id: Optional[int] = None
    nome: Optional[str] = None
    cognome: Optional[str] = None
    cf: Optional[str] = None 
    email: Optional[str] = None
    attivo: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

class Utenti_insert(BaseModel):
    nome: str
    cognome: str
    cf: str
    email: str
    attivo: bool
    password: str
    numero_tel: str