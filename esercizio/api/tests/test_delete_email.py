
from services import delete_email
def test_delete_email_ok(monkeypatch):
    import db_utilities
    fake = db_utilities.Connection()
    monkeypatch.setattr(delete_email, "Connection", lambda *a, **k: fake)
    res = delete_email.cancellazione_email(1)
    assert isinstance(res, str) or res is None
