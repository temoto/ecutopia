create table shop_brand (
	id text not null check (trim(id) <> ''),
	is_deleted boolean not null default false,
	created_at timestamp(0) without time zone not null
		default (utcnow()),
	modified_at timestamp(0) without time zone not null
		default (utcnow()),
	name_ref text,
	description_ref text,
	images json,
	aux json,

	primary key (id)
);


create table shop_product (
	id text not null check (trim(id) <> ''),
	is_active boolean not null default false,
	is_deleted boolean not null default false,
	created_at timestamp(0) without time zone not null
		default (utcnow()),
	modified_at timestamp(0) without time zone not null
		default (utcnow()),
	rank int not null default 0,
	article text,
	name_ref text,
	description_ref text,
	price numeric,
	tags text[],
	images json,
	brand text references shop_brand on delete set null,
	meta_title_ref text,
	meta_description_ref text,
	aux json, -- @json(is_free_shipping:boolean, old_price:numeric, volume:real, weight:real)

	primary key (id)
);
create index on shop_product (is_active, created_at desc, rank);


create table shop_product_relation (
	product1_id text not null references shop_product deferrable initially deferred,
	product2_id text not null references shop_product deferrable initially deferred,
	is_active boolean not null default false,
	is_deleted boolean not null default false,
	created_at timestamp(0) without time zone not null
		default (utcnow()),
	modified_at timestamp(0) without time zone not null
		default (utcnow()),
	cart_count int not null default 0,
	order_count int not null default 0,
	manual int not null default 0,
	rank int not null default 0,
	aux json,

	primary key (product1_id, product2_id)
);
create index on shop_product_relation (is_active, product1_id, product2_id, rank desc);
