create table images
(
	id serial not null
		constraint photos_pkey
			primary key,
	user_id integer,
	image_src varchar(128)
);

alter table images owner to matcha;
