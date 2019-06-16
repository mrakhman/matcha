create table profile_views
(
	id serial not null
		constraint profile_views_pkey
			primary key,
	user_id integer not null,
	checker_id integer not null,
	created_at timestamp not null
);

alter table profile_views owner to matcha;

