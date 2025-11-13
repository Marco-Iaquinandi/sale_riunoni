from models.prenotazioni import Prenotazioni
from db_utilities import Connection
import config


def lettura_prenotazioni(codice_prenotazioni):
    c = Connection(config.host, config.port, config.database, config.username, config.password)
    if codice_prenotazioni is not None:
        q1 = f"""
        where cod_prenotazione = '{codice_prenotazioni}'
        """ 
    else:
        q1 = ' '
    query = f'''
    Select * from prenotazioni {q1}
    '''
    try:
        results = c.fetch_query(query)
        if not results:
            return "non esiste"
        listone = []
        for x in results:
            valori_dict = {
                    "cod_prenotazione": x[0],
                    "cod_sala": x[1],
                    "cf_utente": x[2],
                    "giorno": x[3],
                    "fascia_oraria": x[4],
                    "partecipanti_previsti": x[5],
                    "created_at": x[6]
                }
            listone.append(Prenotazioni(**valori_dict))
        return listone
    except Exception as e:
        print(e)
        return "errore"