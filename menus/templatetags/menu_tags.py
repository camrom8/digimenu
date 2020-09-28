from decimal import Decimal

from django import template

from menus.models import Price, ProductInCart, Quantity

register = template.Library()


@register.simple_tag
def quantity_in_cart(cart, item_id):
    """returns the total amount of products"""
    total = cart.pop(str(item_id), 0)
    return total
