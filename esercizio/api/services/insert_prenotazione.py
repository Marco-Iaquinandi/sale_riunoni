from models.prenotazioni import PrenotazioniInsert
from db_utilities import Connection
import config
from datetime import date
import json
from services.conf_sender import conf_sender



lun_ven = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
weekend = ['saturday', 'sunday']
allways = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def inserimento_prenotazione(item: PrenotazioniInsert):
    fascia_desiderata = []
    c = Connection(config.host, config.port, config.database, config.username, config.password)
    lista_pazza = [item.cf_utente, item.nom_sala, item.giorno, item.fascia_oraria, item.partecipanti_previsti]
    for x in lista_pazza:
        if x is None or x == "" or x == "string":
            return "campi non inseriti"
        if item.partecipanti_previsti <= 0:
            return "min_p"
        else:
            cf = item.cf_utente; giorno = item.giorno.strftime("%Y-%m-%d"); f_oraria = item.fascia_oraria; p_previsti = item.partecipanti_previsti
            sql = f'''select cf,email from utenti where lower(cf) = lower('{item.cf_utente}') AND attivo = True'''
            try:
                q = c.fetch_query(sql)[0][0]
                email =c.fetch_query(sql)[0][1]
            except IndexError:
                return "errore_presenza"
            except Exception as e:
                print(e)
                return "errore_query"
            if q == []:
                return "errore_presenza"
            else: 
                if item.giorno < date.today():
                    return "ins_non_valido"
                else:
                    day_name = item.giorno.strftime("%A").lower()
                    print(day_name)
                    sql = f'''select disponibilita_giorni,capienza from sale where lower(nome) = lower('{item.nom_sala}') '''
                    try:
                        q = c.fetch_query(sql)[0][0]
                        f = c.fetch_query(sql)[0][1]
                        print(q)
                    except IndexError as e:
                        return "ins_non_valido"
                    except Exception as e:
                        return "errore_query"
                    if q == 'LUN-VEN':
                        q = lun_ven
                    if q == 'WEEKEND':
                        q = weekend
                    if q == 'ALLWAYS':
                        q = allways
                    if day_name != "saturday" and day_name != "sunday":
                        fascia_desiderata.append("LUN-VEN")
                        fascia_desiderata.append("ALLWAYS")
                    else:
                        fascia_desiderata.append("WEEKEND")
                        fascia_desiderata.append("ALLWAYS")
                    body_risposta = f''' with antonio as (
                                            select max(id_audit) as antonioculo, s.cod_sala from audit a
                                            join prenotazioni p on p.cod_prenotazione = a.cod_prenotazione
                                            join sale s on p.cod_sala = s.cod_sala
                                            group by s.cod_sala
                                            )

                                            select s.nome
                                            from sale s
                                            left join antonio a on a.cod_sala = s.cod_sala
                                            left join prenotazioni p on p.cod_sala = s.cod_sala
                                            left join audit au on au.cod_prenotazione = p.cod_prenotazione
                                                where (
                                                (split_part(s.disponibilita_ore::text,' - ',2))::time >= (split_part('{item.fascia_oraria}',' - ',2))::time
                                                and
                                                (split_part(s.disponibilita_ore::text,' - ',1))::time <= (split_part('{item.fascia_oraria}',' - ',1))::time 
                                                )
                                                and
                                                capienza >= {item.partecipanti_previsti}
                                                and
                                                (disponibilita_giorni = '{fascia_desiderata[0]}' or disponibilita_giorni = 'ALLWAYS')
                                                and 
                                                (au.operazione != 'PRENOTAZIONE_EFFETTUATA' or au.operazione is null)
                                                and 
                                                (a.antonioculo = au.id_audit or au.id_audit is null)
                                            limit 1
                                        '''
                    if day_name in q:
                        print("coincidenza tra date trovata")
                        sql = f''' select date_part('hour',(split_part(disponibilita_ore::text,'-',2))::time) as fine,date_part('hour',(split_part(disponibilita_ore::text,'-',1))::time) as inizio from sale where lower(nome) = lower('{item.nom_sala}') '''
                        try:
                            rif_max = c.fetch_query(sql)[0][0]
                            rif_min = c.fetch_query(sql)[0][1]
                        except Exception as e:
                            print(e)
                            return "errore_query"
                        if float(item.fascia_oraria[:2]) < int(rif_max) and float(item.fascia_oraria.split("-")[1][:2]) <= int(rif_max) and float(item.fascia_oraria[:2]) >= int(0+(rif_min)):
                            if item.partecipanti_previsti <= f:
                                sql = f'''select p.cod_prenotazione, a.operazione
                                            from prenotazioni p
                                            join audit a on a.cod_prenotazione = p.cod_prenotazione
                                            where p.cod_sala = (select cod_sala from sale where lower(nome) = lower('{item.nom_sala}') limit 1)
                                            and p.giorno = '{item.giorno}'::date
                                            and not (
                                                (split_part(p.fascia_oraria::text,' - ',2))::time <= (split_part('{item.fascia_oraria}',' - ',1))::time
                                                or (split_part('{item.fascia_oraria}',' - ',2))::time <= (split_part(p.fascia_oraria::text,' - ',1))::time
                                            )
                                            order by a.created_at desc
                                            limit 1
                                            '''
                                try:
                                    ris = c.fetch_query(sql)
                                except Exception as e:
                                    print(e)
                                    return "errore_query"
                                if ris != []:
                                    q = ris[0][0]
                                    stato = ris[0][1]
                                if not ris or stato == "PRENOTAZIONE_CANCELLATA" or stato == "CHECKOUT_EFFETTUATO":
                                    sql = f'''insert into prenotazioni(cod_sala,cf_utente,giorno,fascia_oraria,partecipanti_previsti)
                                                values
                                                    ( (select cod_sala from sale where lower(nome) = lower('{item.nom_sala}')), '{item.cf_utente}', '{item.giorno}', '{item.fascia_oraria}', {item.partecipanti_previsti})
                                                    RETURNING cod_prenotazione;    
                                            '''
                                    cod_p = c.fetch_query(sql)[0][0]
                                    sql2 = f'''insert into audit (operazione,who_created,cod_prenotazione,id_utente)
                                            values ('PRENOTAZIONE_EFFETTUATA',
                                                    'UTENTE',
                                                    '{cod_p}'
                                                    ,(select id from utenti where lower(cf) = lower('{item.cf_utente}'))
                                                    )'''
                                    try:
                                        conf_sender(email,item.nom_sala,f_oraria,p_previsti,cod_p)
                                        w = c.query_executor2(sql2)
                                        print(w)
                                        return "prenotato_con_successo"
                                    except Exception as e:
                                        print(e)
                                        return "errore_query"                                
                                else:
                                    
                                    try:
                                        nome_sala = c.fetch_query(body_risposta)[0][0]
                                    except IndexError as e:
                                        return "nessun_risultato_trovato"
                                    except Exception as e:
                                        print("uhmamm1")
                                        print(e)
                                        return "errore_query" 
                                    if nome_sala == []:
                                        return "nessun_risultato_trovato"
                                    else:
                                        sala_consigliata = {
                                                            "cf_utente": f'''{item.cf_utente}''',
                                                            "nom_sala": f"{nome_sala}",
                                                            "giorno": f"{giorno}",
                                                            "fascia_oraria": f"{item.fascia_oraria}",
                                                            "partecipanti_previsti": item.partecipanti_previsti
                                                            }
                                        return "sala_occupata",json.dumps(sala_consigliata)
                            else:
                                try:
                                    nome_sala = c.fetch_query(body_risposta)[0][0]
                                    print(body_risposta)
                                except IndexError as e:
                                    return "nessun_risultato_trovato"
                                except Exception as e:
                                    print("uhmamm2")
                                    print(e)
                                    return "errore_query" 
                                if nome_sala == []:
                                    return "nessun_risultato_trovato"
                                else:
                                    sala_consigliata = {
                                                        "cf_utente": f"{item.cf_utente}",
                                                        "nom_sala": f"{nome_sala}",
                                                        "giorno": f"{giorno}",
                                                        "fascia_oraria": f"{item.fascia_oraria}",
                                                        "partecipanti_previsti": item.partecipanti_previsti
                                                        }
                                    return "sala_occupata",json.dumps(sala_consigliata)
                        else:
                            try:
                                nome_sala = c.fetch_query(body_risposta)[0][0]
                                print(body_risposta)
                            except IndexError as e:
                                return "nessun_risultato_trovato"
                            except Exception:
                                print("uhmamm3")
                                return "errore_query" 
                            if nome_sala == []:
                                return "nessun_risultato_trovato"
                            else:
                                sala_consigliata = {
                                                    "cf_utente": f"{item.cf_utente}",
                                                    "nom_sala": f"{nome_sala}",
                                                    "giorno": f"{giorno}",
                                                    "fascia_oraria": f"{item.fascia_oraria}",
                                                    "partecipanti_previsti": item.partecipanti_previsti
                                                    }
                                return "sala_occupata",json.dumps(sala_consigliata)
                    else:
                        try:
                            nome_sala = c.fetch_query(body_risposta)[0][0]
                        except IndexError as e:
                            return "nessun_risultato_trovato"
                        except Exception:
                            print("uhmamm4")
                            return "errore_query" 
                        if nome_sala == []:
                            return "nessun_risultato_trovato"
                        else:
                            sala_consigliata = {
                                                "cf_utente": f"{item.cf_utente}",
                                                "nom_sala": f"{nome_sala}",
                                                "giorno": f"{giorno}",
                                                "fascia_oraria": f"{item.fascia_oraria}",
                                                "partecipanti_previsti": item.partecipanti_previsti
                                                }
                            return "sala_occupata",json.dumps(sala_consigliata)
