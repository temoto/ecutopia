import argparse
import datetime
import os
import subprocess
import sys

import logbook

import ecutopia.app
import helpers


cmdline = argparse.ArgumentParser()
cmdline.add_argument('--create-db', action='store_true', default=False)
cmdline.add_argument('--drop-db', action='store_true', default=False)
cmdline.add_argument('--quiet', action='store_true', default=False)
cmdline.add_argument('--verbose', action='store_true', default=False)

log = logbook.Logger('migrate')


def apply(key, path):
    log.info('Applying {0} from {1}'.format(key, path))
    params = {
        'id': key,
        'started_at': datetime.datetime.utcnow(),
        'finished_at': None,
    }
    # TODO: stream
    with open(path, 'rb') as f:
        content = f.read().decode('utf-8')
    with helpers.db.transaction() as cursor:
        cursor.execute(content)
        # TODO: data.insert()
        sql = 'insert into migration (id, started_at) values (%(id)s, %(started_at)s)'
        cursor.execute(sql, params)
    params['finished_at'] = datetime.datetime.utcnow()
    helpers.db.execute('update migration set finished_at = %(finished_at)s where id = %(id)s', params)


def psql(cmd):
    sys.stdout.flush()
    sys.stderr.flush()
    p = subprocess.Popen(
        'psql -d postgres',
        stdin=subprocess.PIPE,
        shell=True,
    )
    p.communicate((cmd + '\n').encode('utf-8'))
    sys.stdout.flush()
    sys.stderr.flush()
    return p.poll()


def drop_create(flags, app):
    dsn = helpers.db.parse_dsn(app.config['DATABASE_DEFAULT_DSN'])

    if flags.drop_db:
        log.info('Drop database')
        psql('drop database if exists {db}'.format(db=dsn.dbname))
        flags.create_db = True

    if helpers.db.ping():
        # database exists
        return

    if flags.create_db:
        log.info('Create database')
        psql('create database {db}'.format(db=dsn.dbname))


def enumerate_migration_files(path):
    '''-> [(group, key, full path), ...]

    Example: ('create', 'create/11-auth.sql', '/path/to/backend/db/create/11-auth.sql')
    '''
    items = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        group = os.path.split(dirpath)[-1]
        for filename in filenames:
            key = os.path.join(group, filename)
            path = os.path.join(dirpath, filename)
            items.append((group, key, path))

    items.sort()
    return items


def main():
    # Allow others to import this file for enumerate_migration_files()
    # without depending on generated/model.py
    from . import data

    flags = cmdline.parse_args()

    app = ecutopia.app.init(
        exit=False,
        quiet=flags.quiet,
        verbose=flags.verbose,
        init_db=False,
    )

    with app.app_context():
        drop_create(flags, app)

        available = enumerate_migration_files(app.config['paths']['migration'])
        registered = []
        if helpers.db.table_exists('migration'):
            registered = data.migration_query()
        else:
            log.warning('Table migration does not exist')
        registered_map = {m.id: m for m in registered}

        for (group, key, path) in available:
            m = registered_map.get(key)
            if m and m.finished_at:
                log.debug('Migration {0} is already applied, skip'.format(key))
            else:
                apply(key, path)

if __name__ == '__main__':
    main()
