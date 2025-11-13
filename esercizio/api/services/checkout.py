from db_utilities import Connection
import config
from services.read_utenti import lettura_utenti
from services.read_prenotazioni import lettura_prenotazioni

def checkout_prenotazione(cod_prenotazione):
    c = Connection(config.host, config.port, config.database, config.username, config.password)
    prenotazione = lettura_prenotazioni(cod_prenotazione)
    if prenotazione == "non esiste":
        return "prenotazione 404"
    else:
        utente = lettura_utenti(prenotazione[0].cf_utente)
        if utente == "non esiste" or utente.attivo is False:
            return "utente 404"
        else:
            sql = f"""select * from audit 
            where operazione = 'CHECKOUT_EFFETTUATO' or operazione = 'PRENOTAZIONE_CANCELLATA' and cod_prenotazione = '{prenotazione[0].cod_prenotazione}' and id_utente = {utente.id}"""
            select = c.fetch_query(sql)
            if select == []:
                sql =f"""insert into audit (operazione, who_created, cod_prenotazione, id_utente) values
                ('CHECKOUT_EFFETTUATO', 'UTENTE', '{prenotazione[0].cod_prenotazione}', {utente.id})"""
                try:
                    c.query_executor(sql)
                    return "checkout effettuato"
                except Exception as e:
                    print(e)
            else:
                return "checkout gia effettuato"
