
from services import checkout
def test_checkout_ok(monkeypatch):
    import db_utilities
    fake = db_utilities.Connection()
    # Simula lettura prenotazione esistente non già checkout
    # route in service likely queries audit/prenotazioni
    fake.responses = {"from prenotazioni": [("cod", "sala","cf","2025-10-10","08:00 - 09:00",1,"2025-10-01")],
                      "from audit": []}
    monkeypatch.setattr(checkout, "Connection", lambda *a, **k: fake)
    res = checkout.checkout_prenotazione("7ca2bb16-63cd-43fa-b823-f0aaec168e2a")
    assert isinstance(res, str)
