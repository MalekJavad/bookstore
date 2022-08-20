from django import template

register = template.Library()


@register.filter
def to_capitalize(value, starter):
    return f'{starter}: {value.capitalize()}'
