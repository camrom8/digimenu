from decimal import Decimal

from django import template

from menus.models import Price

register = template.Library()


@register.simple_tag
def quantity_in_cart(cart, item_id):
    """returns the current url with the prefix"""
    sizes = cart.keys()
    prices = [price.id for price in Price.objects.filter(id__in=sizes, item__id=item_id)]
    total = 0
    for price in prices:
        if price:
            total += int(cart[str(price)]['quantity'])
    return total
