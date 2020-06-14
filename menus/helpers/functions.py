import urllib
from django.utils.translation import gettext as _
from time import time

def whatsapp_url(order, phone):
    """Create whatsapp url with order"""
    # Whatsapp message with property information
    message = order
    message_parsed = urllib.parse.quote(message)
    url = "https://wa.me/57{}?text={}".format(phone, message_parsed)
    return url


def to_currency(price=0):
    """returns the current url with the prefix"""
    price_str = str(price)
    if len(price_str) > 3:
        price_currency = '$' + price_str[:-3] + '.' + price_str[-3:]
    else:
        price_currency = '$' + price_str
    return price_currency