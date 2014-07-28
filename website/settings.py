OSU_IMAGE_FORMAT_SMALL = "http://b.ppy.sh/thumb/%d.jpg"
OSU_IMAGE_FORMAT_LARGE = "http://b.ppy.sh/thumb/%dl.jpg"

try:
    from website.settings_local import *
except ImportError:
    pass
