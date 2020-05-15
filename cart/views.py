from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from menus.models import Item
from shop.models import Product
from .cart import Cart
from shop.forms import CartAddProduct


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Item, id=product_id)
    kwargs = {'prod_id': product.id}
    print(request.POST)
    form = CartAddProduct(request.POST, **kwargs)
    print(form.is_valid())
    if form.is_valid():
        print("added product********")
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=True,
                 )
        cart.save()
    return redirect('menu:list')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
            print(item)
            kwargs = {'prod_id': item['product'].id}
            item['update_quantity_form'] = CartAddProduct(
                              initial={'quantity': item['quantity'],
                              'update': True,}, **kwargs)
    return render(request, 'cart/detail.html', {'cart': cart})
