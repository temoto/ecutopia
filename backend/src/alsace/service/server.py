import argparse

import werkzeug.serving

import ecutopia.app


def dev(host, port, app):
    ecutopia.app.log_init(quiet=False, verbose=True)
    werkzeug.serving.run_simple(
        host, port, app,
        use_debugger=True,
        use_reloader=True)


def prod(host, port, app):
    # TODO: fapws3 or something
    werkzeug.serving.run_simple(
        host, port, app,
        processes=16)


def main():
    # TODO: configurable host, port
    host = '127.0.0.1'
    port = 8080
    import ecutopia.wsgi
    dev(host, port, ecutopia.wsgi.app)

if __name__ == '__main__':
    main()
