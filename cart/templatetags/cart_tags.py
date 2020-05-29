from django import template

register = template.Library()


@register.simple_tag
def to_currency(price=0):
    """returns the current url with the prefix"""
    price_str = str(price)
    price_len = len(price_str)
    price_currency = ""
    for i in range(price_len):
        if not (i) % 3:
            price_currency = "." + price_currency
        price_currency = price_str[price_len - 1- i] + price_currency
    price_currency = "$" + price_currency[:-1]
    return price_currency
