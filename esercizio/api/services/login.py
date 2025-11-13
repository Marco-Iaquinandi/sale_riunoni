from db_utilities import Connection
import config
import hashlib
 
 
def verifica_accesso(email,password):
    c = Connection(config.host, config.port, config.database, config.username, config.password)
    p_h = hashlib.sha256(password.encode()).hexdigest()
    sql = f''' select 1 from utenti
            where email = '{email}' and pass = '{p_h}' and attivo = true
            '''
    try:
        results = c.fetch_query(sql)
        if results == []:
            return "non_autenticato"
        if results[0][0] == 1:
            return "autenticato"
    except Exception as e:
        return "errore_query"