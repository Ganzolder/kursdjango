from django import template

register = template.Library()


@register.filter
def status_class(value):
    if value == 'active':
        return 'active'
    return 'inactive'
