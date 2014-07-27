from daemon.handlers.simpleftp import SimpleFTPHandler
SERVERS = (
    {
        'handler': SimpleFTPHandler,
        'server_id': 1,
        'config': {
            'host': 'localhost',
            'username': 'anonymous',
            'password': '',
            'cwd': '/var/www/',
            'url_base': 'http://localhost/',
        }
    },
)

OSU_ACCOUNT = {
    'username': 'player',
    'password': 'password',
}

FETCH_QUEUE_KEY = 'osubeatmap-crawling-queue'
DOWNLOAD_SLEEP_TIME = 300.0
# load local settings
try:
    from daemon.settings_local import *
except ImportError:
    pass
