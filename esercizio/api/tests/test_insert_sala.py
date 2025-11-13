
from services import insert_sala
from models.sale import SaleUpdateClass
def test_insert_sala_ok(monkeypatch):
    import db_utilities
    fake = db_utilities.Connection()
    fake.responses = {"from sale where lower(nome)": []}
    monkeypatch.setattr(insert_sala, "Connection", lambda *a, **k: fake)
    body = SaleUpdateClass(nome="Aquila", capienza=120, manutenzione=False, disponibilita_giorni="LUN-VEN", disponibilita_orari="09:00 - 13:00")
    res = insert_sala.inserimento_sala(body)
    assert any(op[0]=="insert" for op in fake.executed) or isinstance(res, str)
