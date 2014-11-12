OSU_IMAGE_FORMAT_SMALL = "http://b.ppy.sh/thumb/%d.jpg"
OSU_IMAGE_FORMAT_LARGE = "http://b.ppy.sh/thumb/%dl.jpg"

PROXY_DOWNLOAD_SERVERS = [
    # {
    # 'source_server_index': 0,
    #     'regex': '',
    #     'replace': '',
    #     'name': '',
    #     'location': '',
    # },
]

EXTERNAL_SEARCH_URL_FORMAT = ""

try:
    from website.settings_local import *
except ImportError:
    pass
