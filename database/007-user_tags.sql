create table user_tags
(
	user_id integer not null,
	tag_id integer not null,
	constraint user_tags_pkey
		primary key (user_id, tag_id)
);

alter table user_tags owner to matcha;

