create table auth_group (
	id text not null,
	name text,
	is_active boolean not null default false,
	is_deleted boolean not null default false,
	created_at timestamp(0) without time zone not null
		default (utcnow()),
	modified_at timestamp(0) without time zone not null
		default (utcnow()),
	aux json,

	primary key (id)
);


create table auth_user (
	id text not null,
	name text,
	email text,
	phone text,
	admin_comment text,
	is_active boolean not null default false,
	is_deleted boolean not null default false,
	last_login_ips inet[],
	last_login_at timestamp(0) without time zone,
	last_cart_at timestamp(0) without time zone,
	last_order_at timestamp(0) without time zone,
	created_at timestamp(0) without time zone not null
		default (utcnow()),
	modified_at timestamp(0) without time zone not null
		default (utcnow()),
	aux json,

	primary key (id)
);


create table auth_user_group (
	user_id text not null references auth_user deferrable initially deferred,
	group_id text not null references auth_group deferrable initially deferred,
	created_at timestamp(0) without time zone not null
		default (utcnow()),
	modified_at timestamp(0) without time zone not null
		default (utcnow()),
	aux json,

	primary key (user_id, group_id)
);


create table auth_auth (
	user_id text not null references auth_user deferrable initially deferred,
	kind text not null,
	value text,
	created_at timestamp(0) without time zone not null
		default (utcnow()),
	modified_at timestamp(0) without time zone not null
		default (utcnow()),
	aux json,

	primary key (user_id, kind)
);
create index on auth_auth (user_id, modified_at);


create table session (
	id text not null,
	created_at timestamp(0) without time zone not null
		default (utcnow()),
	modified_at timestamp(0) without time zone not null
		default (utcnow()),
	user_id text references auth_user deferrable initially deferred,
	data json,

	primary key (id)
);
