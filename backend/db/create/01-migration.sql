create table migration (
	id text not null check (trim(id) <> ''),
	started_at timestamp without time zone not null
		default (now() at time zone 'utc'),
	finished_at timestamp,
	aux json,

	primary key (id)
);
