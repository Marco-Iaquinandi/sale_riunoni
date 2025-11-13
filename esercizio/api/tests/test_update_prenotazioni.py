
from services import update_prenotazioni
from models.prenotazioni import PrenotazioniInsert
def test_update_prenotazione_ok(monkeypatch):
    import db_utilities
    fake = db_utilities.Connection()
    monkeypatch.setattr(update_prenotazioni, "Connection", lambda *a, **k: fake)
    body = PrenotazioniInsert(cf_utente="CFX", nom_sala="Sala X", giorno=None, fascia_oraria="11:00 - 12:00", partecipanti_previsti=3)
    res = update_prenotazioni.modifica_prenotazione(body, "CODPREN")
    assert isinstance(res, (str, type(None)))
