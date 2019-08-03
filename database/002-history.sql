create table history
(
	id serial not null
		constraint history_pkey
			primary key,
	user_id integer not null,
	profile_id integer not null,
	created_at timestamp default now() not null
);

alter table history owner to matcha;

