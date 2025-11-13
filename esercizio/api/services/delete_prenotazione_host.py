from db_utilities import Connection
import config
from services.read_prenotazioni import lettura_prenotazioni
from services.read_utenti import lettura_utenti

def cancellazione_prenotazione(cod_prenotazione):
    c = Connection(config.host, config.port, config.database, config.username, config.password)
    prenotazione = lettura_prenotazioni(cod_prenotazione)
    if prenotazione == "non esiste":
        return "prenotazione 404"
    else:
        utente = lettura_utenti(prenotazione[0].cf_utente)
        if utente == "non esiste":
            return "utente 404"
        else:
            sql = f"""select * from audit 
            where operazione = 'PRENOTAZIONE_CANCELLATA' and cod_prenotazione = '{prenotazione[0].cod_prenotazione}' and id_utente = {utente.id}"""
            select = c.fetch_query(sql)
            if select == []:
                sql = f"""insert into audit (operazione, who_created, cod_prenotazione, id_utente) values
                    ('PRENOTAZIONE_CANCELLATA', 'SISTEMA', '{prenotazione[0].cod_prenotazione}', {utente.id})"""
                try:
                    c.query_executor(sql)
                    return "prenotazione cancellata"
                except Exception as e:
                    print(e)
            else:
                return "Gia eliminata"