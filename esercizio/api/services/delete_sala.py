from db_utilities import Connection
import config

def cancellazione_sala(cod_sala):
    c = Connection(config.host, config.port, config.database, config.username, config.password)
    sql = f"delete from sale where cod_sala = '{cod_sala}'"
    try:
        esec = c.query_executor2(sql)
        return esec
    except Exception as e:
        print(e)