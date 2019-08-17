create or replace procedure update_users_rating()
	language plpgsql
as $$
DECLARE user_id int;
    begin
        FOR user_id in SELECT id FROM users
        LOOP
            call update_user_rating(user_id);
        end loop;
    end;

$$;

alter procedure update_users_rating() owner to matcha;
