import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from menus.helpers.functions import whatsapp_url, to_currency
from menus.models import Item, Price, ProductInCart
from .cart import Cart
from menus.forms import CartAddProduct
from django.utils.translation import gettext_lazy as _
from time import time
from django.views.generic import View

from .forms import DetailsForm


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
        size_short = size[:4]
        if size_short in ['Only', 'Solo', 'Uniq', 'solo', 'uniq', 'Only']:
            order += f"{item['quantity']}x{product_name} {add_ons_str}: ${item['total_price']},%0A"
        else:
            order += f"{item['quantity']}x{product_name}({size_short})-{add_ons_str}: ${item['total_price']}, "
        if not phone:
            phone = item['product'].price.item.menu.owner.profile.phone
    order = "¡Hola! He hecho mi pedido por Digimenú Colombia y es el siguiente:%0A" + order[
                                                                                      :-2] + f" Total: ${cart.get_total_price()}"
    # print(order)
    wurl = whatsapp_url(order, str(phone))
    # print(wurl)
    return render(request, 'cart/detail.html', {'cart': cart, 'wurl': wurl})


class DeliveryDetails(View):
    def get(self, request):
        form = DetailsForm()
        return render(request, 'cart/delivery.html', {'form': form, })

    def post(self, request):
        form = DetailsForm(request.POST)
        if form.is_valid():
            cart = Cart(request)
            order = ""
            name = ""
            address = ""
            comments = ""
            tips = ""
            pickup = form.cleaned_data["pickup"]
            phone = 0
            tip = int(form.cleaned_data["tip"])
            if form.cleaned_data["name"]:
                name = f'Nombre: {form.cleaned_data["name"]}\n'
            if form.cleaned_data["address"]:
                address = f'Dirección: {form.cleaned_data["address"]}\n'
            if form.cleaned_data["comments"]:
                comments = f'comentarios: {form.cleaned_data["comments"]}\n'
            if tip:
                tips = f'propina: {to_currency(tip)}\n'
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
                size_short = size[:4]
                if size_short in ['Only', 'Solo', 'Uniq', 'solo', 'uniq', 'Only']:
                    order += f"{item['quantity']}x{product_name} {add_ons_str}: ${item['total_price']},\n"
                elif add_ons_str:
                    order += f"{item['quantity']}x{product_name}({size_short})-{add_ons_str}: ${item['total_price']},\n"
                else:
                    order += f"{item['quantity']}x{product_name}({size_short}): ${item['total_price']},\n"
                if not phone:
                    phone = item['product'].price.item.menu.owner.profile.phone
            order = "¡Hola! He hecho mi pedido por Digimenú y es el siguiente:\n" + \
                    order[:-2] + "\n"
            total = f"Total: {to_currency(cart.get_total_price() + tip)}\n"
            details = name + address + comments + tips + pickup + "\n" + total
            wurl = whatsapp_url(order + details, str(phone))
            return HttpResponse(json.dumps({'wupMsg': wurl}), content_type='application/json')
        else:
            return render(request, 'cart/delivery.html', {'form': form})
