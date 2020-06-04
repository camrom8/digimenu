import csv
import io
import time
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.generic import CreateView, ListView, TemplateView, DetailView, FormView

from cart.cart import Cart
from menus.forms import MenuForm, CategoryForm, EstablishmentForm, ItemForm, ItemPriceFormSet, MenuUploadForm
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

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        cart = Cart(request)
        for item in cart:
            if item['product'].price.item.menu != self.get_object():
                keys = request.session['cart'].keys()
                for item in ProductInCart.objects.filter(id__in=keys):
                    item.delete()
                cart.clear()
                break
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

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
    prices_for_product = Price.objects.filter(item__id=item_id)
    if command == "-1":
        size_ids = [size_id for size_id in prices_for_product.values_list('id', flat=True)]
        prices = [product.price for product in
                  ProductInCart.objects.filter(price__id__in=size_ids, id__in=keys).select_related('price')]
        prices_ids = [price.id for price in prices]
        if len(set(prices_ids)) == 1:
            print("here")
            return JsonResponse({'id': prices[0].id})
        message = _("Which size would you like to remove?")
    else:
        prices = prices_for_product
        message = _("How hungry are you?")
    prices_dict = {}
    if len(prices) == 1:
        return JsonResponse({'id': str(prices[0].id)})
    for price in prices:
        prices_dict[price.id] = _(price.size) + " " + price.price_str

    return JsonResponse({'list': prices_dict, 'msg': message})


@csrf_exempt
def get_adds_on(request, item_id):
    price = Price.objects.get(id=item_id)
    adds_ons = AddsOn.objects.filter(product__id=item_id)
    return render(request, "chunks/adds_on.html", {'adds': adds_ons, 'product': price})


@csrf_exempt
def same_items_in_cart(request, item_id):
    keys = request.session['cart'].keys()
    products_in_cart = ProductInCart.objects.filter(price__id=item_id, id__in=keys).select_related('price')
    if not AddsOn.objects.filter(product__id=item_id).exists() and len(products_in_cart) > 0:
        return JsonResponse({'id': str(products_in_cart[0].id), 'product_in_cart': 1})
    if products_in_cart:
        products_dict = {}

        if request.POST['command'] == "1":
            products_dict = {'0': [_('new')]}
        for product in products_in_cart:
            add_ons = ""
            for quantity in product.quantity_set.all().select_related('addOn'):
                qty = quantity.quantity
                if qty == 1:
                    add_ons += quantity.addOn.name + "-"
                else:
                    add_ons += quantity.addOn.name + '(' + str(qty) + ')-'
            add_ons = add_ons[:-1]
            if len(add_ons) > 30:
                adds_list = add_ons.split('-')
                rows = []
                row = ''
                for add in adds_list:
                    if len(row + add) <= 30:
                        row += add + ', '
                    else:
                        rows.append(row)
                        row = add + ', '
                rows.append(row)
                rows[-1] = rows[-1][:-2]
                products_dict[product.id] = [product.price.size + ': ' + rows[0]]
                for row in rows[1:]:
                    products_dict[product.id].append(row)
            else:
                products_dict[product.id] = [product.price.size[:3] + ': ' + add_ons]
        if len(products_dict) == 1:
            return JsonResponse({'id': str(products_in_cart[0].id)})
        return render(request, "chunks/select_product.html", {'products': products_dict, 'id': item_id})
        # return JsonResponse({'list': products_dict, 'msg': _('Select a product'), 'id': item_id})
    return JsonResponse({'id': item_id})


@csrf_exempt
def item_to_order(request, item_id):
    add_ons = request.POST.copy()
    add_ons.pop('csrfmiddlewaretoken', None)
    total = add_ons.pop('grand_total', None)
    total_add_ons = 0

    price = Price.objects.get(id=item_id)
    product_in_cart = ProductInCart.objects.create(price=price, total=int(total[0]))

    add_ons_dict = {add_on: int(value) for add_on, value in add_ons.items() if value != "0"}

    for add_id, qty in add_ons_dict.items():
        add_on = AddsOn.objects.get(id=add_id)
        added = Quantity.objects.create(product=product_in_cart, addOn=add_on, quantity=qty)
        total_add_ons += added.price
    product_in_cart.total = total_add_ons + price.price
    product_in_cart.save()

    return JsonResponse({'item_id': product_in_cart.id, 'price_id': price.item.id})


@login_required
def menu_upload(request):
    template = 'uploads/menu.html'
    if request.method == 'POST':
        form = MenuUploadForm(request.POST or None, request.FILES or None)
        print(form.is_valid())
        if form.is_valid():
            # get form data
            csv_file = form.cleaned_data['csv_file']
            # get user adding properties
            # get csv data
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File must be format:  .CVS')
                print("file error")
                return redirect(reverse('menu:upload'))
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            menu_data = csv.reader(io_string, delimiter=",", quotechar="|")
            # create property, address, images
            for column in menu_data:
                # check if item already exists
                menu = Menu.objects.get(id=column[1])
                if not Item.objects.filter(upload_code=column[0], menu=menu):
                    # create item
                    column[4] = column[4].replace('-', ',')
                    category = Category.objects.get(id=column[2])
                    item, _ = Item.objects.get_or_create(upload_code=column[0], menu=menu, category=category,
                                                         name=column[3], ingredients=column[4], description=column[5]
                                                         )
                    # create price
                    price, _ = Price.objects.get_or_create(item=item, price=column[6], price_str=column[7])
                else:
                    # get item
                    item = Item.objects.get(upload_code=column[0], menu=menu)
                    # update item
                    item.__dict__.update(menu__id=column[1], category=column[2], name=column[3], ingredients=column[4])
                    # get price
                    try:
                        price = Price.objects.filter(item=item)[:1].get()
                        price.__dict__.update(price=column[6], price_str=column[7])
                        price.save()
                    except:
                        print(f'item:{item} does not have price assigned')
                        price, _ = Price.objects.get_or_create(item=item, price=column[6], price_str=column[7])
                        print(f'price has been assigned to item:{item}')
                    # update price

                item.save()

            return HttpResponseRedirect(reverse('menu:details', kwargs={'title_slug': menu.title_slug}))
    form = MenuUploadForm()
    return render(request, template, {'form': form})
