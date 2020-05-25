import urllib
from django.utils.translation import gettext as _


def whatsapp_url(order, phone):
    """Create whatsapp url with order"""
    # Whatsapp message with property information
    message = order
    message_parsed = urllib.parse.quote(message)
    url = "https://wa.me/57{}?text={}".format(phone, message_parsed)
    return url
