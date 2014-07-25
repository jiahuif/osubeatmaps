import tempfile
from os import path

COOKIE_JAR_DUMP_FILE = path.join(tempfile.gettempdir(), 'osu-crawler-cookie-jar.tmp')
# load local settings
try:
    from crawler.settings_local import *
except ImportError:
    pass
