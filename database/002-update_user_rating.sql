create or replace procedure update_user_rating(user_id integer)
	language plpgsql
as $$
DECLARE basic_rating int;
            likes_rating double precision;
    begin
        basic_rating := (
            (bio_text is not null)::int +
            (tags is not null and ARRAY_LENGTH(tags, 1) > 0)::int+
            (profile_image is not null)::int
            ) as rating from users where id = user_id;

        likes_rating :=  ranking.rank FROM (
            SELECT id, percent_rank() over (order by COALESCE(s.likes, 0) + COALESCE(f.likes, 0)) as rank
                        FROM users
                        LEFT JOIN (
                            SELECT f_party as like_id, COUNT(*) as likes
                            FROM likes
                            WHERE s2f
                            GROUP BY f_party
                            ) as f ON users.id = f.like_id
                        LEFT JOIN (
                            SELECT s_party as like_id, COUNT(*) as likes
                            FROM likes
                            WHERE f2s
                            GROUP BY s_party
                            ) as s ON users.id = s.like_id
            ) as ranking
                        where ranking.id = user_id;
        RAISE log 'Likes rating is: %', likes_rating;
        UPDATE users
        SET rating = (basic_rating + FLOOR(7 * likes_rating))
        WHERE id = user_id;

    end;

$$;

alter procedure update_user_rating(integer) owner to matcha;

