from django.template import Library

from website.settings import OSU_IMAGE_FORMAT_LARGE, OSU_IMAGE_FORMAT_SMALL


register = Library()


@register.filter(name='split_difficulties')
def split_difficulties(value, splitter=','):
    return value.split(splitter)


@register.filter(name='osu_thumb_small')
def osu_thumb_small(beatmap_id):
    return OSU_IMAGE_FORMAT_SMALL % int(beatmap_id)


@register.filter(name='osu_thumb_large')
def osu_thumb_large(beatmap_id):
    return OSU_IMAGE_FORMAT_LARGE % int(beatmap_id)
