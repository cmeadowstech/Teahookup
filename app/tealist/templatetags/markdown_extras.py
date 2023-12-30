from django import template
from django.template.defaultfilters import stringfilter
from .extensions import TailwindExtension

import markdown as md

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(
        value, extensions=["markdown.extensions.fenced_code", TailwindExtension()]
    )
