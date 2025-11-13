from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class R_sale(BaseModel):
    nome: str
    capienza: int
    disponibilita_ore: str
    disponibilita_giorni: str


class Sale(BaseModel):
    cod_sala: Optional[str] = None
    nome: Optional[str] = None
    capienza: Optional[int] = None
    manutenzione: Optional[bool] = None
    disponibilita_giorni: Optional[Literal['LUN-VEN', 'WEEKEND', 'ALLWAYS']] = None
    disponibilita_orari: Optional[Literal['08:00 - 09:00', '08:00 - 10:00', '08:00 - 11:00', '08:00 - 12:00',
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

class SaleUpdate(BaseModel):
    cod_sala: Optional[str] = None
    nome: Optional[str] = None
    capienza: Optional[int] = None
    manutenzione: Optional[bool] = None
    disponibilita_giorni: Optional[Literal['LUN-VEN', 'WEEKEND', 'ALLWAYS']] = None
    disponibilita_orari: Optional[Literal['08:00 - 09:00', '08:00 - 10:00', '08:00 - 11:00', '08:00 - 12:00',
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
    

class SaleUpdateClass(BaseModel):
    nome: Optional[str] = None
    capienza: Optional[int] = None
    manutenzione: Optional[bool] = None
    disponibilita_giorni: Optional[Literal['LUN-VEN', 'WEEKEND', 'ALLWAYS']] = None
    disponibilita_orari: Optional[Literal['08:00 - 09:00', '08:00 - 10:00', '08:00 - 11:00', '08:00 - 12:00',
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
 
 