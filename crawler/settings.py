import tempfile
from os import path

COOKIE_JAR_DUMP_FILE = path.join(tempfile.gettempdir(), 'osu-crawler-cookie-jar.tmp')
CRAWLER_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"
# load local settings
try:
    from crawler.settings_local import *
except ImportError:
    pass
