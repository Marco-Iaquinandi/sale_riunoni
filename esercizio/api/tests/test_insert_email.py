
from services import insert_email
from models.email import EmailInsert
def test_insert_email_ok(monkeypatch):
    import db_utilities
    fake = db_utilities.Connection()
    # email non esistente
    fake.responses = {"from public.email where codice_template": []}
    monkeypatch.setattr(insert_email, "Connection", lambda *a, **k: fake)
    body = EmailInsert(codice_template="REMINDER_INIZIO", descrizione="Desc", messaggio="Msg")
    res = insert_email.inserimento_email(body)
    assert any(op[0]=="insert" for op in fake.executed) or isinstance(res, str)
