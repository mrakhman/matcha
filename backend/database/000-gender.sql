do $$ begin
  create type gender as enum ('male', 'female');
  alter type gender owner to matcha;
exception
  when duplicate_object then null;
end $$;
