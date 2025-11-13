from models.audit import Audit
from db_utilities import Connection
import config
 
 
def lettura_audit(operazione,created_at):
    c = Connection(config.host, config.port, config.database, config.username, config.password)
   
    if operazione is not None and created_at is None:
        q1 = f"""where LOWER(operazione::text) like replace(replace(LOWER('%{operazione}%'),'-','_'),' ', '_')"""
    elif created_at is not None and operazione is None:
        q1 = f""" where created_at::date = '{created_at}'"""
    elif created_at is not None and operazione is not None:
        q1 = f""" where LOWER(operazione::text) like replace(replace(LOWER('%{operazione}%'),'-','_'),' ', '_') and created_at::date = '{created_at}'"""
    else:
        q1 = ' '
    query = f'''
    Select * from audit {q1}
    '''
    print(query)
    try:
        results = c.fetch_query(query)
        if results == []:
            return "non esiste"
        listone = []
        for x in results: 
            print(x)           
            valori_dict = {
                    "id_audit": x[0],
                    "operazione": x[1],
                    "who_created": x[2],
                    "cod_prenotazione": x[3],
                    "id_utente" : x[4],
                    "created_at": x[5].strftime("%Y-%m-%d %H:%M:%S")
                }
            listone.append(Audit(**valori_dict))
        return listone
    except Exception as e:
        print(e)
        return "errore"