import smtplib
import config as c
from email.message import EmailMessage


def conf_sender(destinatario,nome_sala: str,fascia_oraria: str,n_persone: int,codice_prenotazione: str):
    mes = f"""Subject: Conferma prenotazione
                From: {c.sender_id}
                To: {destinatario}

                Grazie per aver prenotato la sala: {nome_sala} 
                per le ore {fascia_oraria} 
                per {n_persone} persone
                CODICE PRENOTAZIONE= {codice_prenotazione}
                """
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(c.sender_id, c.password_smtp)
    s.sendmail(c.sender_id, destinatario, mes)
    s.quit()
    
    
def conf_delete(destinatario,cod_prenotazione):
    mes = f"""Subject: Conferma cancellazione prenotazione
                From: {c.sender_id}
                To: {destinatario}

                Prenotazione con codice: {cod_prenotazione} eliminata con successo 
                """
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(c.sender_id, c.password_smtp)
    s.sendmail(c.sender_id, destinatario, mes)
    s.quit()