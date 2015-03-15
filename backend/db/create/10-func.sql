create function utcnow() returns timestamp without time zone as $$
	select now() at time zone 'utc';
$$ language sql stable;
