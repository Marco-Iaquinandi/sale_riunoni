from models.sale import SaleUpdateClass
from db_utilities import Connection
import config

def inserimento_sala(item: SaleUpdateClass):
    c = Connection(config.host, config.port, config.database, config.username, config.password)
    sql1 = f'''select * from sale where nome = '{item.nome}' '''
    if item.nome == "" or item.nome is None:
        return "nome_m"
    if item.capienza == "" or item.disponibilita_giorni == "" or item.disponibilita_orari == "":
        return "v_mancanti"
    try:
        res = c.fetch_query(sql1)
    except Exception as e:
        print(e)
        return "errore_query"
    if res == []:
        sql = f'''INSERT INTO public.sale (nome, capienza, manutenzione, disponibilita_giorni, disponibilita_ore)
        VALUES ('{item.nome}', {item.capienza}, {item.manutenzione}, '{item.disponibilita_giorni}', '{item.disponibilita_orari}')
        returning cod_sala
        '''
        try:
            ris = c.query_executor2(sql)
        except Exception as e:
            print(e)
            return "errore_query"
        return ris
    else:
        return "sala_esistente"

