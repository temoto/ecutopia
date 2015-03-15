import flask


def index():
    flask.request.page_title = flask.current_app.config.live().get('site_name')
    context = {
    }
    return flask.render_template('common/index.html', **context)
