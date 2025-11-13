from models.email import Email
from db_utilities import Connection
import config
 
 
def lettura_email(id_email):
    c = Connection(config.host, config.port, config.database, config.username, config.password)
    query = f'''
    Select * from email where id_email = {id_email}
    '''
    print(query)
    try:
        results = c.fetch_query(query)
        if not results:
            return "non esiste"
        valori_dict = {
                "id_email": results[0][0],
                "codice_template": results[0][1],
                "descrizione": results[0][2],
                "messaggio": results[0][3]
            }
        return Email(**valori_dict)
    except Exception as e:
        print(e)
        return "errore"