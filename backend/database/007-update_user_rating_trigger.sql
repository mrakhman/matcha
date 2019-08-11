create or replace function update_user_rating_trigger() returns trigger
	language plpgsql
as $$
BEGIN
    call update_user_rating(new.id);
    RETURN NEW;
END;
$$;

alter function update_user_rating_trigger() owner to matcha;
