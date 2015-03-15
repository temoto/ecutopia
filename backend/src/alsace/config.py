import datetime

# Begin configurable defaults, copy and modify in config_local.py

# DATABASE_DEFAULT_DSN = 'host=localhost port=6432 dbname=ecutopia user=user password=pass'

# enable/disable debug mode
DEBUG = False

# enable/disable testing mode
TESTING = False

# the name and port number of the server.
# Required for subdomain support (e.g.: 'myapp.dev:5000')
# Note that localhost does not support subdomains so setting this to “localhost” does not help.
# Setting a SERVER_NAME also by default enables URL
# generation without a request context but with an application context.
SERVER_NAME = '127.0.0.1:8080'

STATIC_VERSION = 'dev'

PREFERRED_URL_SCHEME = 'http'

# SECRET_KEY = 'EDIT-THIS'
# SESSION_COOKIE_PATH = None
# SESSION_COOKIE_DOMAIN = None

# End configurable defaults, copy and modify in config_local.py


# Begin final settings, do not modify or override these

# If the application does not occupy a whole domain or subdomain
# this can be set to the path where the application is configured to live.
# This is for session cookie as path value. If domains are used, this should be None.
APPLICATION_ROOT = None

# By default Flask serialize object to ascii-encoded JSON.
# If this is set to False Flask will not encode to ASCII and
# output strings as-is and return unicode strings.
# jsonify will automatically encode it in utf-8 then for transport for instance.
JSON_AS_ASCII = False

JSON_SORT_KEYS = True

# If this is set to True (the default) jsonify responses will be pretty printed
# if they are not requested by an XMLHttpRequest object
# (controlled by the X-Requested-With header)
JSONIFY_PRETTYPRINT_REGULAR = True

# LOGGER_NAME = None

# If set to a value in bytes, Flask will reject incoming requests
# with a content length greater than this by returning a 413 status code.
# MAX_CONTENT_LENGTH = None

PROPAGATE_EXCEPTIONS = None

# the lifetime of a permanent session as datetime.timedelta object.
# Starting with Flask 0.8 this can also be an integer representing seconds.
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=2 * 365)

# By default if the application is in debug mode the request context is not popped
# on exceptions to enable debuggers to introspect the data. This can be disabled by this key.
# You can also use this setting to force-enable it for non debug execution which
# might be useful to debug production applications (but also very risky).
# PRESERVE_CONTEXT_ON_EXCEPTION = None

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_NAME = 's1'
SESSION_COOKIE_SECURE = False

# this flag controls how permanent sessions are refreshed.
# If set to True (which is the default) then the cookie is refreshed each request
# which automatically bumps the lifetime.
# If set to False a set-cookie header is only sent if the session is modified.
# Non permanent sessions are not affected by this.
SESSION_REFRESH_EACH_REQUEST = True

# If this is set to True Flask will not execute the error handlers of HTTP exceptions
# but instead treat the exception like any other and bubble it through the exception stack.
# This is helpful for hairy debugging situations where you have to find out
# where an HTTP exception is coming from.
# TRAP_HTTP_EXCEPTIONS = False

# enable/disable x-sendfile
USE_X_SENDFILE = True

# Werkzeug’s internal data structures that deal with request specific data will
# raise special key errors that are also bad request exceptions. Likewise many
# operations can implicitly fail with a BadRequest exception for consistency.
# Since it’s nice for debugging to know why exactly it failed this flag can be used
# to debug those situations. If this config is set to True you will get
# a regular traceback instead.
# TRAP_BAD_REQUEST_ERRORS = False

# End final settings, do not modify or override these


# TODO: decide
# SEND_FILE_MAX_AGE_DEFAULT = 43200
