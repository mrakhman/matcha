create or replace function update_users_rating_trigger() returns trigger
	language plpgsql
as $$
BEGIN
    call update_users_rating();
    IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        RETURN OLD;
    END IF;
END;
$$;

alter function update_users_rating_trigger() owner to matcha;
