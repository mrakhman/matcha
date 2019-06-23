create table likes
(
	f_party integer not null
		constraint likes_users_f_id_fk
			references users,
	s_party integer not null
		constraint likes_users_s_id_fk
			references users,
	f2s boolean default false not null,
	s2f boolean default false not null,
	constraint likes_pk
		primary key (f_party, s_party)
);

comment on table likes is 'f_party should be lower than s_party';

alter table likes owner to matcha;

create trigger trg_rating
	after insert or update
	on likes
	execute procedure update_users_rating_trigger();

