import json

from django.template import Library
from django.utils.safestring import mark_safe


register = Library()


@register.filter(name='json_lines_array')
def json_lines_array(value, trim=True):
    """

    :param value:
    :param trim:
    :type value: str
    """
    lines = value.split('\n')
    out = []
    for line in lines:
        if not trim:
            out.append(line)
        else:
            trimed = line.strip()
            if trimed != '':
                out.append(trimed)
    return mark_safe(json.dumps(out))