create table unlikes
(
	user_id integer not null,
	unliker_id integer not null,
	unliked_at timestamp not null,
	constraint unlikes_pkey
		primary key (user_id, unliker_id)
);

alter table unlikes owner to matcha;

