create table if not exists messages
(
	id serial not null
		constraint messages_pkey
			primary key,
	sender_id integer not null,
	receiver_id integer not null,
	text text not null,
	created_at timestamp default now()
);

alter table messages owner to matcha;
