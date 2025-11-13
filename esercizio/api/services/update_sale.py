from models.sale import SaleUpdateClass
from services.read_sale import lettura_sale
from db_utilities import Connection
import config



def modifica_sala(item: SaleUpdateClass,cod_sala):
    c = Connection(config.host, config.port, config.database, config.username, config.password)
    try:
        r = lettura_sale(cod_sala)
    except Exception as e:
        print (e)
        return "errore_query"
    if r == "non esiste" or r == [] or r is None:
        return "cod_sbagliato"
    else:
        head = f'update sale set'
        where_condition = f"where cod_sala = '{cod_sala}' "
        termini_da_modificare = []
        if item.nome is not None and item.nome != r.nome and item.nome != "string" and item.nome != "":
            termini_da_modificare.append(f"nome = '{item.nome}' ")
        if item.capienza is not None and item.capienza != r.capienza and item.capienza != "string" and item.capienza != "":
            termini_da_modificare.append(f"capienza = {item.capienza} ")
        if item.manutenzione is not None and item.manutenzione != r.manutenzione and item.manutenzione != "string" and item.manutenzione != "":
            termini_da_modificare.append(f"manutenzione = {item.manutenzione} ")
        if item.disponibilita_giorni is not None and item.disponibilita_giorni != r.disponibilita_giorni and item.disponibilita_giorni != "string" and item.disponibilita_giorni != "":
            termini_da_modificare.append(f"disponibilita_giorni = '{item.disponibilita_giorni}' ")
        if item.disponibilita_orari is not None and item.disponibilita_orari != r.disponibilita_orari and item.disponibilita_orari != "string" and item.disponibilita_orari != "":
            termini_da_modificare.append(f"disponibilita_ore = '{item.disponibilita_orari}' ")
        if termini_da_modificare == []:
            print("Non è stato passato nulla")
            return "nessuna_modifica"
        update_string = ", ".join(termini_da_modificare)
        head = f'{head} {update_string} {where_condition}'
        params = (item.cod_sala,item.nome,item.capienza,item.manutenzione,item.disponibilita_giorni,item.disponibilita_orari)
        try:
            c.query_executor(head,params)
            return cod_sala
        except Exception as e:
            print(e)
            return "errore_query"