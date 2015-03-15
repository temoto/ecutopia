import helpers


RegionRegion = helpers.db.make_model(
    table_name='region_region',
    fields=(
        'id',               # text not null check (trim(id) <> ''),
        'is_active',        # boolean not null default false,
        'is_deleted',       # boolean not null default false,
        'created_at',       # timestamp(0) without time zone not null default (utcnow()),
        'modified_at',      # timestamp(0) without time zone not null default (utcnow()),
        'name_ref',         # text,
        'description_ref',  # text,
    ),
)


RegionIp = helpers.db.make_model(
    table_name='region_ip',
    fields=(
        'mask',         # cidr not null,
        'region_id',    # text not null references region_region deferrable initially deferred,
        'is_active',    # boolean not null default false,
        'is_deleted',   # boolean not null default false,
        'created_at',   # timestamp(0) without time zone not null default (utcnow()),
        'modified_at',  # timestamp(0) without time zone not null default (utcnow()),
    ),
)
