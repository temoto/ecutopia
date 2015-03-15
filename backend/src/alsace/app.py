import os
import sys

import flask
import jinja2
import logbook
import psycopg2
import werkzeug
import werkzeug.utils

import ecutopia.route
import helpers


class LogNullHandler(logbook.Handler):
    blackhole = True

    def should_handle(self, record):
        return record.level < self.level


# TODO: get rid of global_state
global_state = [None, None]
log = logbook.Logger(__name__)


def cache_init(app):
    from flask.ext.cache import Cache

    app.cache = Cache(app, config=app.config)

    return True


def log_init(quiet=False, verbose=False):
    log_level = logbook.INFO
    if quiet:
        log_level = logbook.NOTICE
    if verbose:
        log_level = logbook.DEBUG

    # TODO: get rid of global_state
    setup = global_state[1]
    if setup is not None:
        setup.pop_application()

    handler_null = LogNullHandler(
        level=log_level, bubble=False,
    )
    handler_stderr = logbook.StreamHandler(
        stream=sys.stderr, level=log_level,
    )
    setup = global_state[1] = logbook.NestedSetup([
        handler_stderr,
        handler_null,
    ])
    setup.push_application()

    return True


def path_init(paths):
    ok = True
    paths['package'] = os.path.abspath(os.path.dirname(ecutopia.__file__))
    paths['project'] = os.path.abspath(paths['package'] + '/../..')

    paths['migration'] = os.path.abspath(paths['project'] + '/db')
    if not os.path.exists(paths['migration']):
        log.critical('Migration directory does not exist: {0}'.format(paths['migration']))
        ok = False

    paths['template'] = os.path.abspath(paths['project'] + '/template')
    if not os.path.exists(paths['template']):
        log.critical('Template directory does not exist: {0}'.format(paths['template']))
        ok = False

    paths['static'] = os.path.abspath(paths['project'] + '/../frontend/build')
    if not os.path.exists(paths['static']):
        log.critical('Static directory does not exist: {0}'.format(paths['static']))
        ok = False

    return ok


def route_init(app):
    # TODO: clear current rules
    # TODO: lock
    for item in ecutopia.route.routes:
        rule, endpoint, *rest = item
        endpoint = 'ecutopia.' + endpoint
        fun = werkzeug.utils.import_string(endpoint)
        app.add_url_rule(
            rule=rule,
            endpoint=endpoint,
            view_func=fun,
            *rest)

    return True


def init(exit=True, force=False, quiet=False, verbose=False,
         init_db=True, init_settings=True):
    # TODO: get rid of global_state
    app = global_state[0]
    if app is not None and not force:
        return app

    ok = True
    ok &= log_init(quiet=quiet, verbose=verbose)
    paths = {}
    ok &= path_init(paths)

    if not ok and exit:
        sys.exit(1)

    app = flask.Flask(
        'ecutopia',
        template_folder=paths['template'],
        static_folder=None,
    )
    app.jinja_env.undefined = jinja2.StrictUndefined
    app.config.from_object('ecutopia.config')
    app.config.from_pyfile(paths['project'] + '/config_local.py', silent=True)
    app.config['paths'] = paths

    cache_init(app)

    if init_settings:
        import ecutopia.common.data
        # Using config as easily available everywhere object
        # to expose settings stored in database
        app.config.live = ecutopia.common.data.settings_load

    app.static_folder = paths['static']
    app.static_url_path = '/static/v-{0}'.format(app.config['STATIC_VERSION'])
    app.config['STATIC_URL'] = app.static_url_path
    app.add_url_rule(
        app.static_url_path + '/<path:filename>',
        endpoint='static',
        view_func=app.send_static_file)

    route_init(app)

    if init_db:
        # Test DB connection
        with app.app_context():
            if not helpers.db.ping() and exit:
                sys.exit(1)

    global_state[0] = app
    return app
