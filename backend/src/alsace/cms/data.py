import helpers


CmsBlock = helpers.db.make_model(
    table_name='cms_block',
    fields=(
        'block_id',     # text not null,
        'content_ref',  # text not null,
        'is_active',    # boolean not null default false,
        'is_deleted',   # boolean not null default false,
        'created_at',   # timestamp(0) without time zone not null default (utcnow()),
        'modified_at',  # timestamp(0) without time zone not null default (utcnow()),
        'rank',         # int not null default 0,
        'aux',          # json,
    ),
)


CmsPage = helpers.db.make_model(
    table_name='cms_page',
    fields=(
        'id',                    # text not null,
        'url',                   # text not null,
        'is_active',             # boolean not null default false,
        'is_deleted',            # boolean not null default false,
        'created_at',            # timestamp(0) without time zone not null default (utcnow()),
        'modified_at',           # timestamp(0) without time zone not null default (utcnow()),
        'level',                 # int not null default 0,
        'rank',                  # int not null default 0,
        'title_ref',             # text not null,
        'brief_ref',             # text not null,
        'content_ref',           # text not null,
        'parent_id',             # text references cms_page deferrable initially deferred,
        'meta_title_ref',        # text,
        'meta_description_ref',  # text,
        'aux',                   # json,
    ),
)


CmsMenu = helpers.db.make_model(
    table_name='cms_menu',
    fields=(
        'id',           # text not null,
        'block_id',     # text not null,
        'is_active',    # boolean not null default false,
        'is_deleted',   # boolean not null default false,
        'created_at',   # timestamp(0) without time zone not null default (utcnow()),
        'modified_at',  # timestamp(0) without time zone not null default (utcnow()),
        'items',        # json,
        'aux',          # json,
    ),
)


CmsMenuItem = helpers.db.make_model(
    table_name='cms_menu_item',
    fields=(
        'id',           # text not null,
        'menu_id',      # text not null references cms_menu on delete cascade deferrable initially deferred,
        'is_active',    # boolean not null default false,
        'is_deleted',   # boolean not null default false,
        'created_at',   # timestamp(0) without time zone not null default (utcnow()),
        'modified_at',  # timestamp(0) without time zone not null default (utcnow()),
        'level',        # int not null default 0,
        'rank',         # int not null default 0,
        'parent_id',    # text references cms_menu_item deferrable initially deferred,
        'title_ref',    # text not null,
        'content_ref',  # text not null,
        'target',       # json,
        'aux',          # json,
    ),
)
