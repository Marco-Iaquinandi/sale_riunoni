from db_utilities import Connection
import config

def cancellazione_email(id_email):
    c = Connection(config.host, config.port, config.database, config.username, config.password)
    sql = f"delete from email where id_email = '{id_email}'"
    try:
        esec = c.query_executor2(sql)
        return esec
    except Exception as e:
        print(e)