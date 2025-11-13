from models.prenotazioni import PrenotazioniUpdateClass
from services.read_prenotazioni import lettura_prenotazioni
from db_utilities import Connection
import config



def modifica_prenotazione(item: PrenotazioniUpdateClass,cod_prenotazione):
    c = Connection(config.host, config.port, config.database, config.username, config.password)
    try:
        r = lettura_prenotazioni(cod_prenotazione)
    except Exception as e:
        print (e)
        return "errore_query"
    if r == "non esiste" or r == []:
        return "cod_sbagliato"
    else:
        params = (item.cod_sala,item.cf_utente,item.giorno,item.fascia_oraria,item.partecipanti_previsti)
        for x in params:
            if x == "string" or x == "":
                return "nessuna_modifica"
        head = f'update prenotazioni set'
        where_condition = f"where cod_prenotazione = '{cod_prenotazione}' "
        termini_da_modificare = []
        if item.cod_sala is not None and item.cod_sala != r[0].cod_sala:
            termini_da_modificare.append(f"cod_sala = '{item.cod_sala}' ")
        if item.cf_utente is not None and item.cf_utente != r[0].cf_utente:
            termini_da_modificare.append(f"cf_utente = '{item.cf_utente}' ")
        if item.giorno is not None and item.giorno != r[0].giorno:
            termini_da_modificare.append(f"giorno = '{item.giorno}' ")
        if item.fascia_oraria is not None and item.fascia_oraria != r[0].fascia_oraria:
            termini_da_modificare.append(f"fascia_oraria = '{item.fascia_oraria}' ")
        if item.partecipanti_previsti is not None and item.partecipanti_previsti != r[0].partecipanti_previsti and item.partecipanti_previsti > 0:
            termini_da_modificare.append(f"partecipanti_previsti = {item.partecipanti_previsti} ")
        if termini_da_modificare == []:
            print("Non è stato passato nulla")
            return "nessuna_modifica"
        update_string = ", ".join(termini_da_modificare)
        head = f'{head} {update_string} {where_condition}'
        try:
            c.query_executor(head,params)
            return cod_prenotazione
        except Exception as e:
            print(e)
            return "errore_query"