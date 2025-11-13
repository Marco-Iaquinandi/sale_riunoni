
from services.conf_sender import conf_sender, conf_delete
def test_conf_sender_smtp(monkeypatch):
    # Non deve lanciare eccezioni grazie a FakeSMTP
    res = conf_sender("dest@example.com","Sala X","10:00 - 11:00",2,"CODPREN")
    assert res is None or res == "" or isinstance(res, (str,type(None)))
def test_conf_delete_smtp(monkeypatch):
    res = conf_delete("dest@example.com","CODPREN")
    assert res is None or isinstance(res, (str,type(None)))
