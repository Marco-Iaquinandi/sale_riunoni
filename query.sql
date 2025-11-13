create table utenti(
	id serial primary key,
	nome varchar(255),
	cognome varchar(255),
	cf varchar(16) unique,
	email varchar(255),
	attivo boolean,
	created_at timestamp(0) default CURRENT_TIMESTAMP(0),
	updated_at timestamp(0),
	deleted_at timestamp(0)
);
create type days as enum ('LUN-VEN', 'WEEKEND', 'ALLWAYS');
create type hours as enum ('08:00 - 09:00', '08:00 - 10:00', '08:00 - 11:00', '08:00 - 12:00',
							'08:00 - 13:00', '08:00 - 14:00', '08:00 - 15:00', '08:00 - 16:00',
							'09:00 - 10:00', '09:00 - 11:00', '09:00 - 12:00', '09:00 - 13:00',
							'09:00 - 14:00', '09:00 - 15:00', '09:00 - 16:00',
							'10:00 - 11:00', '10:00 - 12:00', '10:00 - 13:00', '10:00 - 14:00',
							'10:00 - 15:00', '10:00 - 16:00',
							'11:00 - 12:00', '11:00 - 13:00', '11:00 - 14:00', '11:00 - 15:00',
							'11:00 - 16:00',
							'12:00 - 13:00', '12:00 - 14:00', '12:00 - 15:00', '12:00 - 16:00',
							'13:00 - 14:00', '13:00 - 15:00', '13:00 - 16:00',
							'14:00 - 15:00', '14:00 - 16:00',
							'15:00 - 16:00');
create table sale(
	cod_sala varchar(36) primary key default gen_random_uuid(),
	nome varchar(255) unique,
	capienza integer,
	manutenzione boolean,
	disponibilita_giorni days,
	disponibilita_ore hours
);
create table prenotazioni(
	cod_prenotazione varchar(36) primary key default gen_random_uuid(),
	cod_sala varchar(36),
	cf_utente varchar(16),
	giorno date,
	fascia_oraria hours,
	partecipanti_previsti integer,
	created_at timestamp(0) default CURRENT_TIMESTAMP(0),
	foreign key (cod_sala) references sale(cod_sala),
	foreign key (cf_utente) references utenti(cf)
);
create type cod_temp as enum ('REMINDER_INIZIO', 'REMINDER_FINE', 'SOLLECITO_CHECKOUT');
create table email(
	id_email serial primary key,
	codice_template cod_temp,
	descrizione varchar(255),
	messaggio text
);
create type ope as enum ('UTENTE_REGISTRATO', 'UTENTE_MODIFICATO', 'UTENTE_RIMOSSO',
						'PRENOTAZIONE_EFFETTUATA', 'PRENOTAZIONE_CANCELLATA',
						'CHECKOUT_EFFETTUATO', 'EMAIL_INVIATA', 'EMAIL_CHECKIN','EMAIL_PRE_CHECKOUT','EMAIL_POST_CHECKOUT');



create type who as enum ('SISTEMA', 'UTENTE', 'BATCH');
create table audit(
	id_audit serial primary key,
	operazione ope,
	who_created who,
	cod_prenotazione varchar(36),
	id_utente integer,
	created_at timestamp(0) default CURRENT_TIMESTAMP(0),
);
--Insert in tabella
INSERT INTO sale (nome, capienza, manutenzione, disponibilita_giorni, disponibilita_ore) VALUES
('Ariete', 120, false, 'LUN-VEN', '09:00 - 14:00'),
( 'Toro', 150, false, 'ALLWAYS', '10:00 - 15:00'),
('Gemelli', 80,  true,  'LUN-VEN', '08:00 - 12:00'),
('Cancro', 200, false, 'WEEKEND', '14:00 - 16:00'),
('Leone', 95,  false, 'ALLWAYS', '09:00 - 15:00'),
('Vergine',130, true,  'LUN-VEN', '08:00 - 16:00'),
('Bilancia', 160, false, 'ALLWAYS', '13:00 - 16:00'),
('Scorpione', 70,  false, 'WEEKEND', '11:00 - 13:00'),
('Sagittario', 180, false, 'ALLWAYS', '08:00 - 14:00'),
('Capricorno', 110, true,  'LUN-VEN', '10:00 - 16:00'),
('Acquario', 140, false, 'WEEKEND', '12:00 - 16:00'),
('Pesci', 90,  false, 'ALLWAYS', '09:00 - 15:00');