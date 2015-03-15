create table currency_currency (
	id text not null check (trim(id) <> ''),
	is_active boolean not null default false,
	is_deleted boolean not null default false,
	created_at timestamp(0) without time zone not null
		default (utcnow()),
	modified_at timestamp(0) without time zone not null
		default (utcnow()),
	rate_1usd numeric,
	name_ref text,
	description_ref text,
	images json,
	aux json,

	primary key (id)
);


create table currency_history (
	currency_id text not null references currency_currency deferrable initially deferred,
	day date not null,
	created_at timestamp(0) without time zone not null
		default (utcnow()),
	rate_1usd numeric,
	aux json,

	primary key (currency_id, day)
);
