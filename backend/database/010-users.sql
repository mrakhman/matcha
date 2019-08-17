create table if not exists users
(
	id serial not null
		constraint users_pkey
			primary key,
	username varchar(42) not null,
	email varchar(42) not null,
	first_name varchar(20),
	last_name varchar(25),
	gender gender,
	sex_pref varchar(10) default 'bi'::character varying not null,
	password char(94) not null,
	dob timestamp,
	bio_text text,
	profile_image varchar(128),
	last_connection timestamp,
	rating integer default 0 not null,
	tags character varying[] default ARRAY[]::integer[] not null,
	activated boolean default false not null,
	latitude numeric,
	longitude numeric
);

alter table users owner to matcha;

do $$ begin
	create trigger trg_rating
    after insert or update of bio_text, profile_image, tags
		on users
		for each row
		execute procedure update_user_rating_trigger();
	exception
  	when others then null;
end $$;
