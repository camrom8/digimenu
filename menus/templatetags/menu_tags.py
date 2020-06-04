from decimal import Decimal

from django import template

from menus.models import Price, ProductInCart, Quantity

register = template.Library()


@register.simple_tag
def quantity_in_cart(cart, item_id):
    """returns the total amount of products"""
    total = 0
    for item in cart:
        product = cart[item]['product']
        if product.price.item.id == item_id:
            total += cart[item]['quantity']
    return total
