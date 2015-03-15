import decimal

from . import json, model


def test_import_model_01():
    result = list(model.import_models('''
create table foo (
    id serial primary key,
    name text
);
'''))
    expected = '''\
Foo = helpers.db.make_model(
    table_name='foo',
    fields=(
        'id',    # serial primary key,
        'name',  # text
    ),
)
'''
    assert len(result) == 1
    assert result[0][0] == 'Foo'
    assert result[0][1] == expected


def test_import_model_multiline():
    result = list(model.import_models('''
create table foo2 (
    id text not null check (trim(id) <> ''),
    created_at timestamp(0) without time zone not null
        default (utcnow()),
    primary key (id)
);
'''))
    expected = '''\
Foo2 = helpers.db.make_model(
    table_name='foo2',
    fields=(
        'id',          # text not null check (trim(id) <> ''),
        'created_at',  # timestamp(0) without time zone not null default (utcnow()),
    ),
)
'''
    assert len(result) == 1
    assert result[0][0] == 'Foo2'
    assert result[0][1] == expected


def test_import_json_description():
    result = list(model.import_models('''
create table foo3 (
    aux json -- @json(description:text, discount:numeric)
);
'''))
    expected = '''\
Foo3 = helpers.db.make_model(
    table_name='foo3',
    fields=(
        'aux',  # json_fields
    ),
    json_fields=(
        ('aux', 'description', 'text'),
        ('aux', 'discount', 'numeric'),
    ),
)
'''
    assert len(result) == 1
    assert result[0][0] == 'Foo3'
    assert result[0][1] == expected


def test_json_fields():
    Pizza = model.make_model(
        table_name='pizza',
        fields=(
            'id',
            'aux',  # json_fields
        ),
        json_fields=(
            ('aux', 'count', 'int'),
            ('aux', 'price', 'numeric'),
            ('aux', 'title', 'text'),
        ),
    )

    aux_data = {'count': 44, 'price': decimal.Decimal('88.99'), 'title': 'Anger'}
    pizza1 = Pizza(12, json.dumps(aux_data))
    assert pizza1.aux_count == aux_data['count']
    assert pizza1.aux_price == aux_data['price']
    assert pizza1.aux_title == aux_data['title']
