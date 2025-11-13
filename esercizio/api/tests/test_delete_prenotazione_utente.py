
from services import delete_prenotazione_utente
def test_delete_prenotazione_utente_ok(monkeypatch):
    import db_utilities
    fake = db_utilities.Connection()
    monkeypatch.setattr(delete_prenotazione_utente, "Connection", lambda *a, **k: fake)
    monkeypatch.setattr(delete_prenotazione_utente, "lettura_prenotazioni",
                        lambda cod: [type("P", (), {"cod_prenotazione":cod,"cf_utente":"CFX"})()])
    monkeypatch.setattr(delete_prenotazione_utente, "lettura_utenti",
                        lambda cf: type("U", (), {"id":1,"email":"x@y","attivo":True})())
    res = delete_prenotazione_utente.cancellazione_prenotazione_utente("COD")
    assert isinstance(res, str)
