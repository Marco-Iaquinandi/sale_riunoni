from models.email import Email,EmailU
from services.read_email import lettura_email
from db_utilities import Connection
import config



def modifica_email(item: EmailU,id_email):
    c = Connection(config.host, config.port, config.database, config.username, config.password)
    try:
        r = lettura_email(id_email)
    except Exception as e:
        print (e)
        return "errore_query"
    if r == "non esiste" or r == []:
        return "cod_sbagliato"
    else:
        head = f'update email set'
        where_condition = f"where id_email = {id_email} "
        termini_da_modificare = []
        if item.codice_template is not None and item.codice_template != r.codice_template and item.codice_template != "string" and item.codice_template != "":
            termini_da_modificare.append(f"codice_template = '{item.codice_template}' ")
        if item.descrizione is not None and item.descrizione != r.descrizione and item.descrizione != "string" and item.descrizione != "":
            termini_da_modificare.append(f"descrizione = '{item.descrizione}' ")
        if item.messaggio is not None and item.messaggio != r.messaggio and item.messaggio != "string" and item.messaggio != "":
            termini_da_modificare.append(f"messaggio = '{item.messaggio}' ")
        if termini_da_modificare == []:
            print("Non è stato passato nulla")
            return "nessuna_modifica"
        update_string = ", ".join(termini_da_modificare)
        head = f'{head} {update_string} {where_condition}'
        params = (item.codice_template,item.descrizione,item.messaggio)
        try:
            c.query_executor(head,params)
            return id_email
        except Exception as e:
            print(e)
            return "errore_query"