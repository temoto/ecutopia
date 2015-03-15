create table cms_block (
	block_id text not null,
	content_ref text not null,
	is_active boolean not null default false,
	is_deleted boolean not null default false,
	created_at timestamp(0) without time zone not null
		default (utcnow()),
	modified_at timestamp(0) without time zone not null
		default (utcnow()),
	rank int not null default 0,
	aux json,

	primary key (block_id, content_ref)
);
create index on cms_block (is_active, block_id, rank, content_ref);


create table cms_page (
	id text not null,
	url text not null,
	is_active boolean not null default false,
	is_deleted boolean not null default false,
	created_at timestamp(0) without time zone not null
		default (utcnow()),
	modified_at timestamp(0) without time zone not null
		default (utcnow()),
	level int not null default 0,
	rank int not null default 0,
	title_ref text not null,
	brief_ref text not null,
	content_ref text not null,
	parent_id text references cms_page deferrable initially deferred,
	meta_title_ref text,
	meta_description_ref text,
	aux json,

	primary key (id)
);
create index on cms_page (is_active, level, rank, id);
create index on cms_page (is_active, url, id);


create table cms_menu (
	id text not null,
	block_id text not null,
	is_active boolean not null default false,
	is_deleted boolean not null default false,
	created_at timestamp(0) without time zone not null
		default (utcnow()),
	modified_at timestamp(0) without time zone not null
		default (utcnow()),
	items json,
	aux json,

	primary key (id)
);


create table cms_menu_item (
	id text not null,
	menu_id text not null references cms_menu on delete cascade deferrable initially deferred,
	is_active boolean not null default false,
	is_deleted boolean not null default false,
	created_at timestamp(0) without time zone not null
		default (utcnow()),
	modified_at timestamp(0) without time zone not null
		default (utcnow()),
	level int not null default 0,
	rank int not null default 0,
	parent_id text references cms_menu_item deferrable initially deferred,
	title_ref text not null,
	content_ref text not null,
	target json,
	aux json,

	primary key (id)
);
create index on cms_menu_item (is_active, menu_id, level, rank, id);
