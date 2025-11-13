from models.email import EmailU
from db_utilities import Connection
import config
import json
 
def inserimento_email(item: EmailU):
    c = Connection(config.host, config.port, config.database, config.username, config.password)
    dat = (item.codice_template,item.descrizione,item.messaggio)
    sql = '''INSERT INTO public.email (codice_template, descrizione, messaggio)
        VALUES (%s, %s, %s)
        RETURNING email'''
    try:
        if item.codice_template is None and item.descrizione is None and item.messaggio is None:
            return "campi_non_inseriti"
        if item.codice_template is not None and item.descrizione is None or item.descrizione == ""  and item.messaggio is None or item.messaggio == "":
            return "inserire_campi"
        if item.descrizione == "string" or item.messaggio == "string":
            return "inserire_campi_validi"
        else:
            status = c.insert_executor(sql, dat)
        return status
    except Exception as e:
        print(e)
        return "errore query"