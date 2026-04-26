from django import template

register = template.Library()

@register.filter
def mod(value, arg):
    try:
        return int(value) % int(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return ''

@register.filter
def multiply(value, arg):
    try:
        return float(value) * int(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def subint(value, arg):
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return ''