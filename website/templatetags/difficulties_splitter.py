from django.template import Library

register = Library()


@register.filter(name='split_difficulties')
def split_difficulties(value, splitter=','):
    return value.split(splitter)
