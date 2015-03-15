create table shop_list (
	id text not null check (trim(id) <> ''),
	is_active boolean not null default false,
	is_deleted boolean not null default false,
	created_at timestamp(0) without time zone not null
		default (utcnow()),
	modified_at timestamp(0) without time zone not null
		default (utcnow()),
	level int not null default 0,
	rank int not null default 0,
	parent_id text references shop_list deferrable initially deferred,
	name_ref text,
	description_ref text,
	product_count int,
	meta_title_ref text,
	meta_description_ref text,
	images json,
	aux json, -- @json(access:text)

	primary key (id),
	check ((parent_id is null and level = 0) or (parent_id is not null and level > 0))
);
create index on shop_list (is_active, level, rank, id);


create table shop_list_item (
	list_id text not null references shop_list on delete cascade deferrable initially deferred,
	product_id text not null references shop_product on delete cascade deferrable initially deferred,
	is_active boolean not null default false,
	is_deleted boolean not null default false,
	created_at timestamp(0) without time zone not null
		default (utcnow()),
	modified_at timestamp(0) without time zone not null
		default (utcnow()),
	rank int not null default 0,
	name_ref text,
	description_ref text,
	available_regions text[],
	images json,
	aux json, -- @json(discount_percent:numeric, discount_fixed:numeric)

	primary key (list_id, product_id)
);
create index on shop_list_item (is_active, list_id, rank, product_id);
