create table matches
(
	sender_id integer not null,
	receiver_id integer not null,
	is_accepted boolean default false not null,
	is_declined boolean default false not null,
	created_at timestamp not null,
	updated_at timestamp not null,
	constraint matches_pkey
		primary key (sender_id, receiver_id)
);

alter table matches owner to matcha;

