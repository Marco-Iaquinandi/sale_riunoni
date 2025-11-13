from models.utenti import Utenti_insert
from db_utilities import Connection
from datetime import datetime
import config
import hashlib

def inserimento_utente(item: Utenti_insert):
    c = Connection(config.host, config.port, config.database, config.username, config.password)
    dat = (item.nome, item.cognome,item.cf,item.email,item.attivo,item.password,item.numero_tel)
    p_h = hashlib.sha256(item.password.encode()).hexdigest()
    if item.cf  is not None:
        sql = f'''select * from public.utenti where cf = '{item.cf}' '''
        res = c.fetch_query(sql)
    if item.cf == "":
        return "cf_non_inserito"
    if item.nome == "" or item.cognome == "" or item.cf == "" or item.email == "" or item.password == "" or item.numero_tel == "" or item.attivo is None:
        return "nessun_valore_inserito"
    if item.nome == "string" or item.cognome == "string" or item.cf == "string" or item.email == "string" or item.password == "string" or item.numero_tel == "string":
        return "v_base"
    if res == []:
        sql = f'''INSERT INTO public.utenti (nome, cognome, cf, email, attivo,pass,numero_tel)
        VALUES ('{item.nome}','{item.cognome}','{item.cf}','{item.email}',{item.attivo},'{p_h}','{item.numero_tel}')
        RETURNING id
        '''
        id_creato = c.insert_executor(sql, dat)
        sql2 = f"""insert into audit (operazione, who_created, id_utente) values
                ('UTENTE_REGISTRATO', 'SISTEMA', {id_creato})"""
        c.query_executor(sql2)
        return id_creato
    else:
        if res[0][5] is True:
            return "utente_presente"
        elif res[0][5] is False:
            sql = f'''update utenti set attivo = True, updated_at = '{datetime.now()}', deleted_at = Null where cf = '{item.cf}' '''
            try:
                c.query_executor(sql)
                sql2 = f"""insert into audit (operazione, who_created, id_utente) values
                ('UTENTE_MODIFICATO', 'SISTEMA', {res[0][0]})"""
                c.query_executor(sql2)
                return "utente_riattivato"
            except:
                return "errore"
        else :
            return "errore"

