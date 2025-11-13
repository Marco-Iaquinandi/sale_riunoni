from db_utilities import Connection
import config
from datetime import datetime
from services.read_utenti import lettura_utenti
 
def cancellazione_utente_host(cf):
    c = Connection(config.host, config.port, config.database, config.username, config.password)
    sql = f"""update utenti
    set attivo = False,
    updated_at = '{datetime.now()}',
    deleted_at = '{datetime.now()}'
    where cf = '{cf}'"""
    try:
        if lettura_utenti(cf) == "non esiste":
            esec = 'utente 404'
            return esec
        elif lettura_utenti(cf).attivo is False:
            esec = 'Gia Eliminato'
            return esec
        else:
            esec = c.query_executor2(sql)
            sql2 = f"""insert into audit (operazione, who_created, id_utente) values
            ('UTENTE_RIMOSSO', 'SISTEMA', {lettura_utenti(cf).id})"""
            c.query_executor(sql2)
            return esec
    except Exception as e:
        print(e)