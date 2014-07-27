[app:main]
use = egg:{{settings['project:name']}}

{%- if settings['develop'] %}

[server:main]
use = egg:waitress#main
host = 0.0.0.0
port = 6543
{%- endif %}

# Begin logging configuration
[loggers]
keys = root, {{settings['project:name']}}

[handlers]
keys = console, all

[formatters]
keys = generic

[logger_root]
level = DEBUG
handlers = all

[logger_{{settings['project:name']}}]
level = DEBUG
handlers = console
qualname = {{settings['project:name']}}

[logger_routes]
level = DEBUG
handlers = console
qualname = routes.middleware

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = INFO
formatter = generic

[handler_all]
class = handlers.TimedRotatingFileHandler
args = ('{{paths['data:log']}}','midnight', 1)
level = DEBUG
formatter = generic

[formatter_generic]
format = %(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s

# End logging configuration
[uwsgi]
socket = {{paths['uwsgi:socket']}}
master = true

need-app = true
processes = 4
chmod-socket = 777

pythonpath = {{paths['venv:site-packages']}}*.egg
log-slow = true

