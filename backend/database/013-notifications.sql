create table if not exists notifications
(
	id serial not null
		constraint notifications_pk
			primary key,
	user_id integer not null
		constraint notifications_users_id_fk
			references users
				on delete restrict,
	is_read boolean default false not null,
	text text not null,
	created_at timestamp default now() not null,
	type varchar(10) not null
);

alter table notifications owner to matcha;

create unique index if not exists notifications_id_uindex
	on notifications (id);
