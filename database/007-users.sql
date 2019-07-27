create table users
(
	id serial not null
		constraint users_pkey
			primary key,
	username varchar(42) not null,
	email varchar(42) not null,
	first_name varchar(20),
	last_name varchar(25),
	gender varchar(14),
	sex_pref varchar(10),
	password char(94) not null,
	dob timestamp,
	bio_text text,
	profile_image varchar(128),
	last_connection timestamp
);

alter table users owner to matcha;

