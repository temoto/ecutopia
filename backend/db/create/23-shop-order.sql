create table shop_order_status (
	id text not null check (trim(id) <> ''),
	name_ref text,

	primary key (id)
);


create table shop_order (
	id text not null check (trim(id) <> ''),
	user_id text not null references auth_user deferrable initially deferred,
	status_id text not null references shop_order_status deferrable initially deferred,
	is_deleted boolean not null default false,
	created_at timestamp(0) without time zone not null
		default (utcnow()),
	modified_at timestamp(0) without time zone not null
		default (utcnow()),
	sum_price numeric not null,
	comment text,
	created_ip inet,
	discount_fixed numeric,
	discount_percent numeric,
	final_price numeric,
	delivery_id text references shop_delivery_type deferrable initially deferred,
	payment_id text references shop_payment_type deferrable initially deferred,
	user_info json,
	aux json,

	primary key (id)
);


create table shop_order_item (
	order_id text not null references shop_order on delete cascade deferrable initially deferred,
	product_id text not null references shop_product on delete cascade deferrable initially deferred,
	status_id text references shop_order_status deferrable initially deferred,
	is_deleted boolean not null default false,
	created_at timestamp(0) without time zone not null
		default (utcnow()),
	modified_at timestamp(0) without time zone not null
		default (utcnow()),
	price numeric not null,
	discount_fixed numeric,
	discount_percent numeric,
	aux json,

	primary key (order_id, product_id)
);
