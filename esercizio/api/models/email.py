from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class Email(BaseModel):
    id_email: Optional[int] = None
    codice_template: Optional[Literal['REMINDER_INIZIO', 'REMINDER_FINE', 'SOLLECITO_CHECKOUT']] = None
    descrizione: Optional[str] = None
    messaggio: Optional[str] = None
    
    
    
class EmailU(BaseModel):
    codice_template: Optional[Literal['REMINDER_INIZIO', 'REMINDER_FINE', 'SOLLECITO_CHECKOUT']] = None
    descrizione: Optional[str] = None
    messaggio: Optional[str] = None
    
class EmailInsert(BaseModel):
    codice_template: Optional[Literal['REMINDER_INIZIO', 'REMINDER_FINE', 'SOLLECITO_CHECKOUT']] = Field(default=None)
    descrizione: str = Field(default=None)
    messaggio: str = Field(default=None)
    