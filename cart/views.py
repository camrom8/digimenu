from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from menus.helpers.functions import whatsapp_url
from menus.models import Item, Price
from .cart import Cart
from shop.forms import CartAddProduct
from django.utils.translation import gettext_lazy as _


@require_POST
def cart_add(request, price_id):
    cart = Cart(request)
    price = get_object_or_404(Price, id=price_id)
    form = CartAddProduct(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        quantity = cd['quantity']
        # print('quantity')
        # print(quantity)
        qty_current = 0
        cart_current = request.session['cart'].copy()
        item_size = cart_current.pop(str(price_id), False)
        # print("item_size")
        # print(item_size)
        if item_size:
            # print('yes')
            qty_current = item_size['quantity']
        if quantity == -1 and qty_current <= 1:
            cart.remove(price)
            return JsonResponse({'qty': -qty_current})
        cart.add(price=price,
                 quantity=quantity,
                 update_quantity=False,
                 )
        cart.save()
        return JsonResponse({'qty': quantity})
    return JsonResponse({'error': 'there was an error'})


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Price, id=product_id)
    cart.remove(product)
    return JsonResponse({'msg': 'Product Removed', 'id': str(product.item.id), })


def cart_detail(request):
    cart = Cart(request)
    order = ""
    phone = 0
    for item in cart:
        size = _(item['size'])
        order += f"{item['quantity']}x{item['product'].item.name}({size}): {item['total_price']}, "
        if not phone:
            phone = item['product'].item.menu.owner.profile.phone
    order = order[:-2] + f" Total: {cart.get_total_price()}"
    # print(order)
    wurl = whatsapp_url(order, str(phone))
    # print(cart[0]['product'].item.menu.owner)
    return render(request, 'cart/detail.html', {'cart': cart, 'wurl':wurl})
