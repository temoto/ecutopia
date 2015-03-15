create table shop_delivery_type (
	id text not null check (trim(id) <> ''),
	is_active boolean not null default false,
	is_deleted boolean not null default false,
	created_at timestamp(0) without time zone not null
		default (utcnow()),
	modified_at timestamp(0) without time zone not null
		default (utcnow()),
	name_ref text,
	description_ref text,
	is_free boolean not null default false,
	available_regions text[],
	images json,
	aux json, -- @json(free_price_threshold:numeric, free_volume_limit:numeric)

	primary key (id)
);


create table shop_payment_type (
	id text not null check (trim(id) <> ''),
	is_active boolean not null default false,
	is_deleted boolean not null default false,
	created_at timestamp(0) without time zone not null
		default (utcnow()),
	modified_at timestamp(0) without time zone not null
		default (utcnow()),
	name_ref text,
	description_ref text,
	available_regions text[],
	images json,
	aux json,  -- @json(charge_percent:numeric, charge_fixed:numeric)

	primary key (id)
);
