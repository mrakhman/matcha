create or replace function count_intersect(anyarray, anyarray) returns bigint
	language sql
as $$
SELECT COUNT(*) FROM (
        SELECT UNNEST($1)
        INTERSECT
        SELECT UNNEST($2)
    ) as intersecrion;
$$;

alter function count_intersect(anyarray, anyarray) owner to matcha;
