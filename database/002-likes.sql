create table likes
(
	sender_id integer not null,
	receiver_id integer not null,
	like_for_like boolean default false not null,
	created_at timestamp not null,
	updated_at timestamp not null,
	constraint matches_pkey
		primary key (sender_id, receiver_id)
);

alter table likes owner to matcha;

