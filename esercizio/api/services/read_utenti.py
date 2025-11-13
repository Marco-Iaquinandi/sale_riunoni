from models.utenti import Utenti
from db_utilities import Connection
import config


def lettura_utenti(cf):
    c = Connection(config.host, config.port, config.database, config.username, config.password)
    query = f'''
    select * from utenti where lower(cf) = lower('{cf}')
    '''
    try:
        results = c.fetch_query(query)
        if not results:
            return "non esiste"
        utenti_dict = {
            'id': results[0][0],
            'nome': results[0][1],
            'cognome': results[0][2],
            'cf': results[0][3],
            'email': results[0][4],
            'attivo': results[0][5],
            'created_at': results[0][6],
            'updated_at': results[0][7],
            'deleted_at': results[0][8]
        }
        return Utenti(**utenti_dict)
    except Exception as e:
        return "errore"