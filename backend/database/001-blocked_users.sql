create table if not exists blocked_users
(
	blocked_id integer not null,
	blocker_id integer not null,
	constraint blocked_users_pkey
		primary key (blocked_id, blocker_id)
);

alter table blocked_users owner to matcha;
