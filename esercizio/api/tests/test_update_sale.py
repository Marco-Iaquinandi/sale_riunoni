
from services import update_sale
from types import SimpleNamespace
def test_update_sale_ok(monkeypatch):
    import db_utilities
    fake = db_utilities.Connection()
    monkeypatch.setattr(update_sale, "Connection", lambda *a, **k: fake)
    # ensure lettura_sale returns current persisted values to diff against
    monkeypatch.setattr(update_sale, "lettura_sale",
                        lambda cod: type("S", (), {"nome":"Old","capienza":150,"manutenzione":False,
                                                   "disponibilita_giorni":"LUN-VEN","disponibilita_orari":"09:00 - 13:00"})())

    body = SimpleNamespace(nome=None, capienza=200, manutenzione=False, disponibilita_giorni=None, disponibilita_orari=None, cod_sala='SALA')
    res = update_sale.modifica_sala(body, "SALA")
    assert isinstance(res, (str, type(None)))
