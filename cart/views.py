from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from menus.helpers.functions import whatsapp_url
from menus.models import Item, Price, ProductInCart
from .cart import Cart
from menus.forms import CartAddProduct
from django.utils.translation import gettext_lazy as _
from time import time

@csrf_exempt
@require_POST
def cart_add(request, item_id):
    cart = Cart(request)
    item = ProductInCart.objects.get(id=item_id)
    quantity = int(request.POST['quantity'])
    qty_current = 0
    try:
        qty_current = request.session['cart'][str(item_id)]['quantity']
    except KeyError:
        pass
    if quantity == -1 and qty_current <= 1:
        cart.remove(item)
        return JsonResponse({'qty': -qty_current})
    cart.add(item=item,
             quantity=quantity,
             )
    return JsonResponse({'qty': quantity})
    # return JsonResponse({'error': 'there was an error'})



@csrf_exempt
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ProductInCart, id=product_id)
    # print('here')
    cart.remove(product)
    return JsonResponse({'msg': 'Product Removed', 'id': str(product.price.item.id), })


@csrf_exempt
def cart_detail(request):
    cart = Cart(request)
    order = ""
    phone = 0
    for item in cart:
        try:
            product_name = item['product'].price.item.name
        except:
            return render(request, 'cart/detail.html', {'cart': cart})
        add_ons_str = ""
        add_ons = item['product'].add_on.values_list('name', flat=True)
        for add_on in add_ons:
            add_ons_str += add_on + ", "
        add_ons_str = add_ons_str[:-2]
        size = _(item['size'])
        size_short = size[:3]
        order += f"{item['quantity']}x{product_name}({size_short})-{add_ons_str}: ${item['total_price']}, "
        if not phone:
            phone = item['product'].price.item.menu.owner.profile.phone
    order = "¡Hola! He hecho mi pedido por Digimenú Colombia y es el siguiente: " + order[:-2] + f" Total: ${cart.get_total_price()}"
    # print(order)
    wurl = whatsapp_url(order, str(phone))
    print(wurl)
    return render(request, 'cart/detail.html', {'cart': cart, 'wurl': wurl})
