from pydantic import BaseModel, Field,field_serializer
from typing import Optional, Literal
from datetime import datetime, date
from typing import Annotated

DateFormatted = Annotated[
    Optional[datetime], 
    Field(json_schema_extra={"format": "dd/mm/yyyy"})
]


class Prenotazioni(BaseModel):
    cod_prenotazione: Optional[str] = None
    cod_sala: Optional[str] = None
    cf_utente: Optional[str] = None
    giorno: Optional[datetime] = None
    fascia_oraria : Optional[str] = None
    partecipanti_previsti: Optional[int] = None
    created_at: Optional[datetime] = None


class PrenotazioniU(BaseModel):
    cod_prenotazione: Optional[str] = None
    cod_sala: Optional[str] = None
    cf_utente: Optional[str] = None
    giorno: Optional[datetime] = None
    fascia_oraria : Optional[str] = None
    partecipanti_previsti: Optional[int] = None



class PrenotazioniInsert(BaseModel):
    cf_utente: Optional[str] = None
    nom_sala: Optional[str] = None
    giorno: Annotated[
        Optional[date], 
        Field(
            json_schema_extra={
                "type": "string",
                "format": "date",
                "example": "yyyy-mm-dd"
            }
        )
    ] = None
    fascia_oraria: Optional[Literal['08:00 - 09:00', '08:00 - 10:00', '08:00 - 11:00', '08:00 - 12:00',
                        '08:00 - 13:00', '08:00 - 14:00', '08:00 - 15:00', '08:00 - 16:00',
                        '09:00 - 10:00', '09:00 - 11:00', '09:00 - 12:00', '09:00 - 13:00',
                        '09:00 - 14:00', '09:00 - 15:00', '09:00 - 16:00',
                        '10:00 - 11:00', '10:00 - 12:00', '10:00 - 13:00', '10:00 - 14:00',
                        '10:00 - 15:00', '10:00 - 16:00',
                        '11:00 - 12:00', '11:00 - 13:00', '11:00 - 14:00', '11:00 - 15:00',
                        '11:00 - 16:00',
                        '12:00 - 13:00', '12:00 - 14:00', '12:00 - 15:00', '12:00 - 16:00',
                        '13:00 - 14:00', '13:00 - 15:00', '13:00 - 16:00', '19:00 - 21:00',
                        '14:00 - 15:00', '14:00 - 16:00','18:00 - 19:00',
                        '15:00 - 16:00']] = None
    partecipanti_previsti: Optional[int] = None


class PrenotazioniUpdateClass(BaseModel):
    cod_sala: Optional[str] = None
    cf_utente: Optional[str] = None
    giorno: Optional[datetime] = None
    fascia_oraria : Optional[str] = None
    partecipanti_previsti: Optional[int] = None
