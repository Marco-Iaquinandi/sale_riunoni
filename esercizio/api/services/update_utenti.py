from db_utilities import Connection
import config
from datetime import datetime
from services.read_utenti import lettura_utenti
from models.utenti import Utenti, Utenti_insert

def aggiornamento_utente(item: Utenti_insert, cf):
    c = Connection(config.host, config.port, config.database, config.username, config.password)
    get = lettura_utenti(cf)
    if get == "non esiste":
        return "utente 404"
    else:
        if item == Utenti_insert(nome= "string", cognome= "string", cf= "string", email= "string", attivo= True):
            return "nessun update"
        else:
            head = "update utenti set "
            where = f"where lower(cf) = lower('{cf}')"
            costruzione = []
            if item.nome is not None and item.nome != get.nome and item.nome != "" and item.nome != "string":
                costruzione.append(f"nome = '{item.nome}'")
            if item.cognome is not None and item.cognome != get.cognome and item.cognome != "" and item.cognome != "string":
                costruzione.append(f"cognome = '{item.cognome}'")
            if item.cf is not None and item.cf != get.cf and item.cf != "" and item.cf != "string":
                costruzione.append(f"cf = '{item.cf}'")
            if item.email is not None and item.email != get.email and item.email != "" and item.email != "string":
                costruzione.append(f"email = '{item.email}'")
            if item.attivo is not None and item.attivo != get.attivo and item.attivo != "":
                costruzione.append(f"attivo = '{item.attivo}'")
            if costruzione == []:
                return "nessun update"
            else:
                costruzione.append(f"updated_at = '{datetime.now()}'")
                stringa = ", ".join(costruzione)
                head = f"{head} {stringa} {where}"
                ogg = (item.nome, item.cognome, item.cf, item.email, item.attivo)
                try:
                    c.query_executor(head, ogg)
                    sql = f"""insert into audit (operazione, who_created, id_utente) values
                    ('UTENTE_MODIFICATO', 'SISTEMA', {get.id})"""
                    c.query_executor(sql)
                    return "utente modificato"
                except Exception as e:
                    print(e)