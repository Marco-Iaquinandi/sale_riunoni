
from services import delete_prenotazione_host
def test_delete_prenotazione_host_ok(monkeypatch):
    import db_utilities
    fake = db_utilities.Connection()
    monkeypatch.setattr(delete_prenotazione_host, "Connection", lambda *a, **k: fake)
    # patch read_prenotazioni + read_utenti used inside
    from services import read_prenotazioni, read_utenti
    monkeypatch.setattr(delete_prenotazione_host, "lettura_prenotazioni",
                        lambda cod: [type("P", (), {"cod_prenotazione":cod,"cf_utente":"CFX"})()])
    monkeypatch.setattr(delete_prenotazione_host, "lettura_utenti",
                        lambda cf: type("U", (), {"id":1,"email":"x@y"})())
    res = delete_prenotazione_host.cancellazione_prenotazione("COD")
    assert isinstance(res, str)
