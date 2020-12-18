from decimal import Decimal
from django.conf import settings

from menus.helpers.functions import to_currency
from menus.models import Item, Price, ProductInCart


class Cart(object):

    def __init__(self, request):
        """
Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the prices of the products  in the cart and get the products
        from the database.
        """
        prices_ids = self.cart.keys()
        # get the product objects and add them to the cart
        product = ProductInCart.objects.filter(id__in=prices_ids)

        cart = self.cart.copy()
        for price in product:
            cart[str(price.id)]['product'] = price

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, item, quantity=1):
        """
        Add a product to the cart or update its quantity.
        """
        item_id = str(item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {'quantity': 0,
                                  'price': str(item.total),
                                  'size': item.price.size,
                                  'price_str': to_currency(item.total),
                                  }
        self.cart[item_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            prod_in_cart = ProductInCart.objects.get(id=product_id)
            prod_in_cart.delete()

    def get_total_price(self):
        value = sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
        if value < 60000:
            value += 4000
        return value

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
