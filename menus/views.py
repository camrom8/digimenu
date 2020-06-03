from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.generic import CreateView, ListView, TemplateView, DetailView, FormView

from cart.cart import Cart
from menus.forms import MenuForm, CategoryForm, EstablishmentForm, ItemForm, ItemPriceFormSet
from menus.models import Menu, Item, Category, Establishment, Price, AddsOn, ProductInCart, Quantity
from django.utils.translation import gettext_lazy as _


class MenuCreate(CreateView):
    """View to create menu"""
    model = Menu
    form_class = MenuForm
    template_name = "menus/create.html"
    success_url = reverse_lazy('menu:item-create')


class MenuList(ListView):
    """View for displaying all menus"""
    model = Menu
    template_name = "menus/list.html"


class ItemCreate(CreateView):
    """View to create Item"""
    model = Item
    form_class = ItemForm
    template_name = "chunks/item_create.html"
    success_url = reverse_lazy('menu:item-create')

    def form_valid(self, form):
        """valid the other 2 forms, location and property details"""
        context = self.get_context_data()
        prices = context['price']
        if prices.is_valid():
            item = form.save()
            prices.instance = item
            prices.save()
            return super(ItemCreate, self).form_valid(form)
        return super(ItemCreate, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        """Add price inline form"""
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['price'] = ItemPriceFormSet(self.request.POST)
        else:
            context['price'] = ItemPriceFormSet()

        return context

    def get_form_kwargs(self):
        kwargs = super(ItemCreate, self).get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs


class CategoryCreate(CreateView):
    """View to create Category"""
    model = Category
    form_class = CategoryForm
    template_name = "chunks/category_create.html"


class EstablishmentCreate(CreateView):
    """View to create Establishment"""
    model = Establishment
    form_class = EstablishmentForm
    template_name = "chunks/Establishment_create.html"


class ViewTest(TemplateView):
    template_name = "menus/details3.html"


class MenuDetails(DetailView):
    """View Menu with items"""
    model = Menu
    template_name = "menus/details.html"
    slug_url_kwarg = 'title_slug'
    slug_field = 'title_slug'

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     cart = Cart(request)
    #     for item in cart:
    #         if item['product'].item.menu != self.object:
    #             cart.clear()
    #         break
    #     context = self.get_context_data(object=self.object)
    #     return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        """get categories in the context data"""
        context = super().get_context_data(**kwargs)
        categories_id = [item.category.id for item in self.object.items.all().distinct('category__name')]
        categories = Category.objects.filter(id__in=categories_id)
        context['items'] = {}
        for category in categories:
            context['items'][category.name] = [item for item in self.object.items.filter(category=category)]
        return context

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        template_name = self.object.template
        if not template_name:
            template_name = "menus/details2.html"
        return self.response_class(
            request=self.request,
            template=template_name,
            context=context,
            using=self.template_engine,
            **response_kwargs
        )


@csrf_exempt
def item_prices_get(request, item_id):
    """get all the prices for a item """
    command = request.POST['command']
    keys = request.session['cart'].keys()
    if int(command) < 0:
        sizes_id = [size.id for size in Price.objects.filter(item__id=item_id)]
        prices = [product.price for product in ProductInCart.objects.filter(price__id__in=sizes_id, id__in=keys)]
        message = _("Which size would you like to remove?")
        # print(prices)
    else:
        prices = [price for price in Price.objects.filter(item__id=item_id)]
        message = _("How hungry are you?")
    prices_dict = {}
    if len(prices) == 1:
        return JsonResponse({'id': str(prices[0].id)})
    for price in prices:
        prices_dict[price.id] = _(price.size) + " " + price.price_str

    return JsonResponse({'list': prices_dict, 'msg': message})


def get_adds_on(request, item_id):
    price = Price.objects.get(id=item_id)
    adds_ons = AddsOn.objects.filter(product__id=item_id)
    return render(request, "chunks/adds_on.html", {'adds': adds_ons, 'product': price})


def item_to_order(request, item_id):
    add_ons = request.POST.copy()
    # print(add_ons)
    add_ons.pop('csrfmiddlewaretoken', None)
    total = add_ons.pop('grand_total', None)
    price = Price.objects.get(id=item_id)
    product_in_cart = ProductInCart(client=request.user, price=price, total=int(total[0]))
    product_in_cart.save()
    for add_on, qty in add_ons.items():
        if int(qty) > 0:
            add_on_object = AddsOn.objects.get(id=add_on)
            add, _ = Quantity.objects.get_or_create(product=product_in_cart, addOn=add_on_object)
            add.quantity = int(qty)
            add.save()
    total = 0
    for add in Quantity.objects.filter(product=product_in_cart):
        total += add.price
    product_in_cart.total = total + price.price
    product_in_cart.save()
    return JsonResponse({'item_id': product_in_cart.id, 'price_id': price.item.id})


@csrf_exempt
def same_items_in_cart(request, item_id):
    keys = request.session['cart'].keys()
    products_in_cart = ProductInCart.objects.filter(price__id=item_id, id__in=keys)
    if not AddsOn.objects.filter(product__id=item_id) and len(products_in_cart) > 0:
        # print("here")
        return JsonResponse({'id': str(products_in_cart[0].id), 'product_in_cart': 1})
        # if not AddsOn.objects.filter(product__id=item_id):
        #     print("no adds")
        #     add_on = False
    if products_in_cart:
        products_dict = {}
        if int(request.POST['command']) > 0:
            products_dict = {'0': _('new')}
        for product in products_in_cart:
            products_dict[product.id] = product.price.size + ': '
            for quantity in product.quantity_set.all():
                products_dict[quantity.product.id] += quantity.addOn.name + '(' + str(quantity.quantity) + '), '
            products_dict[product.id] = products_dict[product.id][:-2]
        if len(products_dict) == 1:
            return JsonResponse({'id': str(products_in_cart[0].id)})
        return JsonResponse({'list': products_dict, 'msg': _('Select a product'), 'id': item_id})
    return JsonResponse({'id': item_id})
