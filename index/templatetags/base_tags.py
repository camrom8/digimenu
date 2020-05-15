from django import template

register = template.Library()


@register.simple_tag
def remove_url_prefix(url='/'):
    """returns the current url with the prefix"""
    url_no_prefix = url.split('/')[2:]
    return '/'.join(url_no_prefix)
