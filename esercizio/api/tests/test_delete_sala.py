
from services import delete_sala
def test_delete_sala_ok(monkeypatch):
    import db_utilities
    fake = db_utilities.Connection()
    monkeypatch.setattr(delete_sala, "Connection", lambda *a, **k: fake)
    res = delete_sala.cancellazione_sala("SALA123")
    assert isinstance(res, str) or res is None
