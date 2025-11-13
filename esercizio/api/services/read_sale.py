from models.sale import R_sale
from db_utilities import Connection
import config


def lettura_sale(capienza,data,inizio,fine):
    c = Connection(config.host, config.port, config.database, config.username, config.password)
    query = f'''
                select s.nome, s.capienza, s.disponibilita_ore, s.disponibilita_giorni
                from sale s
                where
                    coalesce(s.manutenzione, false) = false
                    
                    and s.capienza >= {capienza}
                    
                    and split_part(s.disponibilita_ore::text, ' - ', 1)::time <= '{inizio}'::time
                    and split_part(s.disponibilita_ore::text, ' - ', 2)::time >= '{fine}'::time
                    
                    and (
                        s.disponibilita_giorni = 'ALLWAYS'
                        or (s.disponibilita_giorni = 'LUN-VEN' and extract(isodow from date '{data}') between 1 and 5)
                        or (s.disponibilita_giorni = 'WEEKEND' and extract(isodow from date '{data}') in (6, 7))
                    )
                    
                    and not exists (
                        select 1
                        from prenotazioni p
                        where p.cod_sala = s.cod_sala
                        and p.giorno = date '{data}'
                        
                        and (split_part(p.fascia_oraria::text, ' - ', 2)::time > '{inizio}'::time)
                        and (split_part(p.fascia_oraria::text, ' - ', 1)::time < '{fine}'::time)
                    )
                order by s.nome;
                '''
    try:
        results = c.fetch_query(query)
        listone = []
        for x in results:
            valori_dict = {
                    "nome": x[0],
                    "capienza": x[1],
                    "disponibilita_ore": x[2],
                    "disponibilita_giorni": x[3]
                }
            listone.append(R_sale(**valori_dict))
        return listone
    except Exception as e:
        print(e)
        return "errore"