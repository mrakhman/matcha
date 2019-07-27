create table tags
(
	id serial not null
		constraint tags_pkey
			primary key,
	tag varchar(32) not null
);

alter table tags owner to matcha;

