import decimal
import re

import logbook
import sql

from . import data, json


RE_CREATE_TABLE = re.compile(
    r'create table (?P<name>[\w_]+) \((?P<definition>.+?)\);',
    re.IGNORECASE | re.DOTALL)
RE_JSON_DEFINITION = re.compile(r'--.+?@json\((\w+):(\w+)(?:,\s*(\w+):(\w+))+\)')

log = logbook.Logger('model')


def json_reader(storage_name, name, db_type, _missing=object()):
    def reader(self, _Decimal=decimal.Decimal):
        if self._json_cache is None:
            self._json_cache = {}

        attr_name = storage_name + '_' + name
        value = self._json_cache.get(attr_name, _missing)
        if value is not _missing:
            return value

        parsed_storage = self._json_cache.get(storage_name, _missing)
        if parsed_storage is _missing:
            parsed_storage = self._json_cache[storage_name] = json.loads(
                getattr(self, storage_name))

        value = parsed_storage.get(name)
        if value is not None:
            if db_type == 'numeric':
                value = _Decimal(value)
        self._json_cache[attr_name] = value
        return value

    return reader


def make_model(table_name, fields, json_fields=(),
               _namedlist=data.namedlist,
               _sql=sql, _sql_table=sql.Table):
    '''TODO
    '''
    model_name = ''.join(s.title() for s in table_name.split('_'))

    model = _namedlist(
        model_name,
        fields,
        attrs={'_json_cache': None},
    )

    for storage, name, db_type in json_fields:
        attr_name = storage + '_' + name
        setattr(model, attr_name, property(json_reader(storage, name, db_type)))

    model._table = table = _sql_table(table_name)

    column_items = [(name, getattr(table, name)) for name in fields]
    model._column_map = dict(column_items)
    model._columns = [v for (_, v) in column_items]

    return model


def parse_json(column, s, _empty=()):
    ''' 'aux json, -- comment @json(foo:text, bar:int)' ->
    ["('aux', 'foo', 'text')", "('aux', 'bar', 'int')"]
    '''
    m = RE_JSON_DEFINITION.search(s)
    if not m:
        return _empty

    groups = m.groups()
    assert len(groups) % 2 == 0
    result = [
        '''{indent}('{0}', '{1}', '{2}'),'''.format(
            column, name, type_,
            indent=' ' * 8,
        )
        for name, type_ in zip(groups[::2], groups[1::2])
    ]
    return result


def import_model(table_name, definition):
    lines = definition.splitlines()

    # join incomplete lines
    lines2 = []
    previous = None
    # TODO: parse tokens
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        if line.startswith('primary key (') or line.startswith('check ('):
            continue
        if line.endswith(','):
            if previous:
                line = previous + ' ' + line
                previous = None
            lines2.append(line)
            continue
        if i == len(lines) - 1:
            lines2.append(line)
        previous = line
    lines = lines2
    if not lines:
        log.error('No columns extracted from table: {0}'.format(
            table_name))

    tokens = [s.split(' ', 1) for s in lines]
    max_column_width = max(len(t[0]) for t in tokens)
    fields = []
    json_fields = []
    for column, rest in tokens:
        jf = parse_json(column, rest)
        if jf:
            rest = 'json_fields'
            json_fields.extend(jf)
        field_text = '''{indent}'{column}',  {pad}# {rest}'''.format(
            indent=' ' * 8,
            column=column,
            pad=' ' * (max_column_width - len(column)),
            rest=rest,
        )
        fields.append(field_text)

    model_name = ''.join(s.title() for s in table_name.split('_'))
    result_lines = [
        '''{model} = helpers.db.make_model('''.format(model=model_name),
        '''    table_name='{table}','''.format(table=table_name),
        ''')\n''',
    ]
    if fields:
        result_lines.insert(-1, '''{indent}fields=(\n{s}\n{indent}),'''.format(
            indent=' ' * 4, s='\n'.join(fields)))
    if json_fields:
        result_lines.insert(-1, '''{indent}json_fields=(\n{s}\n{indent}),'''.format(
            indent=' ' * 4, s='\n'.join(json_fields)))

    result = '\n'.join(result_lines)

    return model_name, result


def import_models(sql_text):
    for m in RE_CREATE_TABLE.finditer(sql_text):
        table_name = m.group('name').strip()
        definition = m.group('definition').strip()
        yield import_model(table_name, definition)
