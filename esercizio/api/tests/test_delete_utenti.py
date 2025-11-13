
from services import delete_utenti_host, delete_utenti_utente
def test_delete_utente_host(monkeypatch):
    import db_utilities
    fake = db_utilities.Connection()
    monkeypatch.setattr(delete_utenti_host, "Connection", lambda *a, **k: fake)
    monkeypatch.setattr(delete_utenti_host, "lettura_utenti",
                        lambda cf: type("U", (), {"id":1,"attivo":True})())
    res = delete_utenti_host.cancellazione_utente_host("CFX")
    assert isinstance(res, str)
def test_delete_utente_utente(monkeypatch):
    import db_utilities
    fake = db_utilities.Connection()
    monkeypatch.setattr(delete_utenti_utente, "Connection", lambda *a, **k: fake)
    monkeypatch.setattr(delete_utenti_utente, "lettura_utenti",
                        lambda cf: type("U", (), {"id":1,"attivo":True})())
    res = delete_utenti_utente.cancellazione_utente("CFX")
    assert isinstance(res, str)
