
import types
import pytest

class FakeSMTP:
    def __init__(self, host, port):
        self.host=host; self.port=port; self.started=False; self.logged=False
    def starttls(self): self.started=True
    def login(self, user, pw): self.logged=True
    def sendmail(self, sender, dest, msg): return {}
    def quit(self): return True

class FakeConnection:
    def __init__(self, *args, **kwargs):
        self.responses = {}
        self.executed = []

    def fetch_query(self, sql: str):
        for key, value in self.responses.items():
            if key.lower() in sql.lower():
                return value
        return []

    def insert_executor(self, sql: str, dat=None):
        self.executed.append(("insert", sql, dat))
        return "ok"

    def query_executor(self, sql: str, params=None):
        self.executed.append(("exec1", sql, params))
        return "ok"

    def query_executor2(self, sql: str, params=None):
        self.executed.append(("exec2", sql, params))
        return "ok"

@pytest.fixture(autouse=True)
def patch_env(monkeypatch):
    # ensure project root on path
    import os, sys, pathlib
    _TESTS_DIR = pathlib.Path(__file__).resolve().parent
    _PROJECT_ROOT = _TESTS_DIR.parent
    if str(_PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(_PROJECT_ROOT))

    # fake config
    fake_cfg = types.SimpleNamespace(
        host="FAKE_HOST", port=5432, database="FAKE_DB",
        username="FAKE_USER", password="FAKE_PASS",
        API_HOST="0.0.0.0", API_PORT=8000,
        sender_id="test@example.com", password_smtp="pwd"
    )
    import builtins
    builtins.config = fake_cfg  # fallback if modules do 'import config as c'
    # patch module attributes
    import importlib, db_utilities
    monkeypatch.setattr(db_utilities, "Connection", lambda *a, **k: FakeConnection())
    # smtplib SMTP mock for conf_sender
    import smtplib
    monkeypatch.setattr(smtplib, "SMTP", lambda host, port: FakeSMTP(host, port))

    return {"FakeConnection": FakeConnection, "FakeSMTP": FakeSMTP, "config": fake_cfg}
