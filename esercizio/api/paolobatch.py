import smtplib
import config
import time
from datetime import datetime
from db_utilities import Connection



while True:
    now = datetime.now().strftime("%H:%M")
    c = Connection(config.host, config.port, config.database, config.username, config.password)
    def sender_email(destinatario,mes):
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(config.sender_id, config.password_smtp)
        s.sendmail(config.sender_id, destinatario, mes)
        s.quit()
    sql2 =f''' with antonio as (
                    select max(id_audit) as antonioculo, s.cod_sala from audit a
                    join prenotazioni p on p.cod_prenotazione = a.cod_prenotazione
                    join sale s on p.cod_sala = s.cod_sala
                    group by s.cod_sala
                    )

                select max(a.id_audit),a.operazione,a.cod_prenotazione
                from audit a
                JOIN prenotazioni p on p.cod_prenotazione = a.cod_prenotazione
                join sale s on s.cod_sala = p.cod_sala 
                JOIN antonio an on an.cod_sala = s.cod_sala
                join utenti u on u.cf = p.cf_utente
                where operazione != 'PRENOTAZIONE_CANCELLATA' and p.giorno = now()::date and (an.antonioculo = a.id_audit)
                group by a.cod_prenotazione,a.operazione'''
    try:
        ultima_op = c.fetch_query(sql2)
    except IndexError as e:
        break
    except Exception as e:
        break
    for y in ultima_op:
        if y[1] == 'PRENOTAZIONE_EFFETTUATA':
            sql = f''' select max(a.id_audit),(((split_part(p.fascia_oraria::text,' - ',1))::time)-'00:15') as invio_pre, u.email,a.cod_prenotazione,a.id_utente
                        from audit a
                        JOIN prenotazioni p on p.cod_prenotazione = a.cod_prenotazione
                        join utenti u on u.cf = p.cf_utente
                        where operazione = 'PRENOTAZIONE_EFFETTUATA' and operazione != 'EMAIL_CHECKIN' and operazione != 'EMAIL_PRE_CHECKOUT' and operazione != 'EMAIL_POST_CHECKOUT' and p.giorno = now()::date and a.cod_prenotazione = '{y[2]}'
                        group by a.cod_prenotazione,a.operazione,p.fascia_oraria,p.giorno, u.email, a.id_utente
                        '''
            try:
                ba = c.fetch_query(sql)
            except IndexError as e:
                break
            except Exception as e:
                break   
            for x in ba:
                try:
                    confr_inv = str(x[1])[:4]
                    if confr_inv[1] == ':': 
                        confr_inv = f"0{confr_inv}"
                    else:
                        confr_inv = str(x[1])[:5] 
                    if now == confr_inv:
                        mes = f"""From: {config.sender_id}
                                    To: {x[2]}
                                    Subject: Conferma prenotazione
                                    MIME-Version: 1.0
                                    Content-Type: text/plain; charset=utf-8
                                    Content-Transfer-Encoding: 8bit

                                    Promemoria Check-in: La sua sala conferenze/riunioni e' pronta. Il check-in e' previsto tra 15 minuti. Si prega di recarsi alla reception o seguire le istruzioni ricevute. Grazie."""
                        sender_email(x[2],mes)
                        query_insert = f'''insert into audit(operazione,who_created,cod_prenotazione, id_utente)
                                            values
                                                ('EMAIL_CHECKIN','BATCH', '{x[3]}',{x[4]})
                                        '''

                        try:
                            c.query_executor2(query_insert)
                        except Exception as e:
                            break  
                        time.sleep(1)
                except IndexError as e:
                    break
                except Exception as e:
                    break
        if y[1] == 'EMAIL_CHECKIN':
            sql3 = f''' select max(a.id_audit),(((split_part(p.fascia_oraria::text,' - ',2))::time)-'00:15') as invio_pre, u.email,a.cod_prenotazione,a.id_utente
                from audit a
                JOIN prenotazioni p on p.cod_prenotazione = a.cod_prenotazione
                join utenti u on u.cf = p.cf_utente
                where operazione = 'EMAIL_CHECKIN' and p.giorno = now()::date and a.cod_prenotazione = '{y[2]}'
                group by a.cod_prenotazione,a.operazione,p.fascia_oraria,p.giorno, u.email,a.id_utente
            '''
            try:
                ba = c.fetch_query(sql3)
            except IndexError as e:
                break
            except Exception as e:
                break   
            for x in ba:
                try:
                    confr_inv = str(x[1])[:4]
                    if confr_inv[1] == ':': 
                        confr_inv = f"0{confr_inv}"
                    else:
                        confr_inv = str(x[1])[:5] 
                    if now == confr_inv:
                        mes = f"""From: {config.sender_id}
                        To: {x[2]}
                        Subject: Conferma prenotazione
                        MIME-Version: 1.0
                        Content-Type: text/plain; charset=utf-8
                        Content-Transfer-Encoding: 8bit

                        Avviso Checkout Imminente: Si prega di notare che l'orario di scadenza della Sua prenotazione e' tra 15 minuti. La preghiamo di liberare la sala per consentire i preparativi successivi. Per estensioni, contatti la reception. Grazie."""
                        sender_email(x[2],mes)
                        query_insert = f'''insert into audit(operazione,who_created, cod_prenotazione, id_utente)
                                            values
                                                ('EMAIL_PRE_CHECKOUT','BATCH', '{x[3]}',{x[4]})
                                        '''

                        try:
                            c.query_executor2(query_insert)
                        except Exception as e:
                            break
                        time.sleep(1)
                except IndexError as e:
                    break
                except Exception as e:
                    break
        if y[1] == 'EMAIL_PRE_CHECKOUT':
            sql4 = f''' select max(a.id_audit),(((split_part(p.fascia_oraria::text,' - ',2))::time)+'00:10') as invio_pre, u.email,a.cod_prenotazione,a.id_utente
                from audit a
                JOIN prenotazioni p on p.cod_prenotazione = a.cod_prenotazione
                join utenti u on u.cf = p.cf_utente
                where operazione = 'EMAIL_PRE_CHECKOUT' and p.giorno = now()::date and a.cod_prenotazione = '{y[2]}'
                group by a.cod_prenotazione,a.operazione,p.fascia_oraria,p.giorno, u.email,a.id_utente
            '''
            try:
                ba = c.fetch_query(sql4)
            except IndexError as e:
                break
            except Exception as e:
                break   
            for x in ba:
                try:
                    confr_inv = str(x[1])[:4]
                    if confr_inv[1] == ':': 
                        confr_inv = f"0{confr_inv}"
                    else:
                        confr_inv = str(x[1])[:5] 
                    if now == confr_inv:
                        mes = f"""From: {config.sender_id}
                                    To: {x[2]}
                                    Subject: Conferma prenotazione
                                    MIME-Version: 1.0
                                    Content-Type: text/plain; charset=utf-8
                                    Content-Transfer-Encoding: 8bit

                                    URGENTE: Checkout Scaduto. La prenotazione della Sua sala è terminata 10 minuti fa. La preghiamo di liberare immediatamente la sala per non incorrere in costi aggiuntivi o disturbare la successiva prenotazione. Contattare la reception per assistenza."""
                        sender_email(x[2],mes)

                        query_insert = f'''insert into audit(operazione,who_created, cod_prenotazione, id_utente)
                                            values
                                                ('EMAIL_POST_CHECKOUT','BATCH', '{x[3]}',{x[4]})
                                        '''

                        try:
                            c.query_executor2(query_insert)
                        except Exception as e:
                            break
                        time.sleep(1)
                except IndexError as e:
                    break
                except Exception as e:
                    break
                
                
