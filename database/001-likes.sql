create table likes
(
	user_id integer not null,
	liker_id integer not null,
	created_at timestamp not null,
	like_for_like boolean not null,
	constraint likes_pkey
		primary key (user_id, liker_id)
);

alter table likes owner to matcha;

