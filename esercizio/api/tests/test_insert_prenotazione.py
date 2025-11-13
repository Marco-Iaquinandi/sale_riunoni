
from services import insert_prenotazione
from models.prenotazioni import PrenotazioniInsert
from datetime import date
def test_insert_prenotazione_minimum_ok(monkeypatch):
    import db_utilities
    fake = db_utilities.Connection()
    # user exists & active
    fake.responses = {
        # utente attivo
        "from utenti where": [("CFX","mail@example.com")],
        # disponibilità e capienza
        "select disponibilita_giorni": [("LUN-VEN", 100)],
        # orari min/max (fine, inizio)
        "date_part('hour'": [(15, 8)],
        # nessuna prenotazione confliggente
        "from prenotazioni": [],
        "insert into prenotazioni": [("COD-GENERATO-TEST",)],
    }
    monkeypatch.setattr(insert_prenotazione, "Connection", lambda *a, **k: fake)
    item = PrenotazioniInsert(
        cf_utente="CFX", nom_sala="Sala X", giorno=date.today(), fascia_oraria="10:00 - 11:00", partecipanti_previsti=2
    )
    res = insert_prenotazione.inserimento_prenotazione(item)
    assert isinstance(res, str)
