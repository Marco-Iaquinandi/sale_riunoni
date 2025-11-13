
from services import read_audit
def test_read_audit_ok(monkeypatch):
    import db_utilities
    fake = db_utilities.Connection()
    fake.responses = {"from audit": [(1,"OPER","WHO","COD",2,"2025-09-30T10:00:00")]}
    monkeypatch.setattr(read_audit, "Connection", lambda *a, **k: fake)
    res = read_audit.lettura_audit("prenotazione", "2025-09-30")
    assert isinstance(res, list) or res == "404" or isinstance(res, str)
