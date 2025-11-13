from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class Audit(BaseModel):
    id_audit: Optional[int] = None
    operazione: Optional[Literal['UTENTE_REGISTRATO', 'UTENTE_MODIFICATO', 'UTENTE_RIMOSSO',
                        'PRENOTAZIONE_EFFETTUATA', 'PRENOTAZIONE_CANCELLATA', 'EMAIL_CHECKIN', 'EMAIL_PRE_CHECKOUT', 'EMAIL_POST_CHECKOUT',
                        'CHECKOUT_EFFETTUATO', 'EMAIL_INVIATA']] = None
    who_created: Optional[Literal['SISTEMA', 'UTENTE', 'BATCH']] = None
    cod_prenotazione: Optional[str] = None
    id_utente: Optional[int] = None
    created_at: Optional[datetime] = None


