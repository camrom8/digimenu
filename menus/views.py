import csv
import io
import time
import unidecode
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.generic import CreateView, ListView, TemplateView, DetailView, FormView, UpdateView

from cart.cart import Cart
from menus.forms import MenuForm, CategoryForm, EstablishmentForm, ItemForm, ItemPriceFormSet, MenuUploadForm, \
    SizeUploadForm
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
    paginate_by = 2

    def get_queryset(self):
        qs = super().get_queryset()
        city = self.kwargs['city']
        category = self.request.GET.get('category')
        if city:
            capitalized_city = city.capitalize()
            unaccented_city = unidecode.unidecode(city)
            city_list = [city, capitalized_city, unaccented_city]
            if category:
                return qs.filter(city__in=city_list, establishment=category)
            return qs.filter(city__in=city_list)
        return qs


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


class ItemUpdate(UpdateView):
    """View to create Item"""
    model = Item
    form_class = ItemForm
    template_name = "chunks/item_create.html"
    success_url = reverse_lazy('menu:edit')

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
        map_url2 = ""
        if "iPhone" in request.META['HTTP_USER_AGENT']:
            map_url = f'https://www.google.com/maps/search/?api=1&query={str(self.object.lat)},{str(self.object.lng)}&query_place_id={self.object.subtitle}'
            map_url2 = f'href="http://maps.apple.com/maps?saddr=Current%20Location&daddr={str(self.object.lat)},{str(self.object.lng)}'
        else:
            map_url = f'https://www.google.com/maps/search/?api=1&query={str(self.object.lat)},{str(self.object.lng)}&query_place_id={self.object.subtitle}'
        cart = Cart(request)
        for item in cart:
            if item['product'].price.item.menu != self.get_object():
                keys = request.session['cart'].keys()
                for item in ProductInCart.objects.filter(id__in=keys):
                    item.delete()
                cart.clear()
                break
        context = self.get_context_data(object=self.object)
        map_url2 = ""
        if "iPhone" in request.META['HTTP_USER_AGENT'] or "iPad" in request.META['HTTP_USER_AGENT'] :
            map_url = f'https://www.google.com/maps/search/?api=1&query={str(self.object.lat)},{str(self.object.lng)}&query_place_id=ChIJMT91T74FP44RRL88gS9dxUA'
            map_url2 = f'href="http://maps.apple.com/maps?saddr=Current%20Location&daddr={str(self.object.lat)},{str(self.object.lng)}'
        else:
            map_url = f'https://www.google.com/maps/search/?api=1&query={str(self.object.lat)},{str(self.object.lng)}&query_place_id=ChIJMT91T74FP44RRL88gS9dxUA'

        context['map_url'] = map_url
        if map_url2:
            context['map_url2'] = map_url2
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        """get categories in the context data"""
        context = super().get_context_data(**kwargs)
        categories_id = self.object.items.values_list('category_id', flat=True).distinct('category')
        categories = Category.objects.filter(id__in=categories_id)
        context['items'] = {}
        for category in categories:
            context['items'][category.name] = \
                [item for item in self.object.items.filter(category=category).order_by('upload_code', 'name')]
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


class MenuEditDetails(DetailView):
    """View Menu with items"""
    model = Menu
    template_name = "menus/edit.html"
    slug_url_kwarg = 'title_slug'
    slug_field = 'title_slug'

    def get_context_data(self, **kwargs):
        """get categories in the context data"""
        context = super().get_context_data(**kwargs)
        categories_id = self.object.items.values_list('category_id', flat=True).distinct('category')
        categories = Category.objects.filter(id__in=categories_id)
        context['items'] = {}
        for category in categories:
            context['items'][category.name] = \
                [item for item in self.object.items.filter(category=category).order_by('upload_code', 'name')]
        return context


@csrf_exempt
def item_prices_get(request, item_id):
    """get all the prices for a item """
    command = request.POST['command']
    keys = request.session['cart'].keys()
    prices_for_product = Price.objects.filter(item__id=item_id).order_by('price')
    if command == "-1":
        size_ids = [size_id for size_id in prices_for_product.values_list('id', flat=True)]
        prices = [product.price for product in
                  ProductInCart.objects.filter(price__id__in=size_ids, id__in=keys).select_related('price')]
        prices_ids = [price.id for price in prices]
        if len(set(prices_ids)) == 1:
            return JsonResponse({'id': prices[0].id})
        message = _("Which size would you like to remove?")
    else:
        prices = prices_for_product
        message = _("Select an option")
    if len(prices) == 1:
        return JsonResponse({'id': str(prices[0].id)})
    prices_dict = {}
    for price in prices:
        prices_dict[price.id] = _(price.size) + " " + price.price_str

    return JsonResponse({'list': prices_dict, 'msg': message})


@csrf_exempt
def get_adds_on(request, item_id):
    """Check if product has addons or choices"""
    price = Price.objects.get(id=item_id)
    adds_ons = AddsOn.objects.filter(product__id=item_id)
    if price.choice:
        return render(request, "chunks/selection.html", {'adds': adds_ons, 'product': price})
    if price.half:
        return render(request, "chunks/halves.html", {'adds': adds_ons, 'product': price})
    return render(request, "chunks/adds_on.html", {'adds': adds_ons, 'product': price})


@csrf_exempt
def same_items_in_cart(request, item_id):
    """Check if the same product is already in cart and return the list"""
    keys = request.session['cart'].keys()
    products_in_cart = ProductInCart.objects.filter(price__id=item_id, id__in=keys).select_related('price')
    if products_in_cart:
        if not AddsOn.objects.filter(product__id=item_id).exists():
            return JsonResponse({'id': str(products_in_cart[0].id), 'product_in_cart': 1})
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
                size = _(product.price.size)
                products_dict[product.id] = [size + ': ' + rows[0]]
                for row in rows[1:]:
                    products_dict[product.id].append(row)
            else:
                size = _(product.price.size)
                products_dict[product.id] = [product.price.item.name + ' ' + size[:3] + ' + ' + add_ons]
        if len(products_dict) == 1:
            return JsonResponse({'id': str(products_in_cart[0].id)})
        return render(request, "chunks/select_product.html", {'products': products_dict, 'id': item_id})
    return JsonResponse({'id': item_id})


@csrf_exempt
def item_to_order(request, item_id):
    """add item to order"""
    add_ons = request.POST.copy()
    # total_add_ons = 0
    total = add_ons.pop('grand_total', None)
    product_in_cart = ProductInCart.objects.create(price_id=item_id, total=int(total[0]))

    selection = add_ons.pop('selection', None)
    if selection:
        Quantity.objects.create(product_id=product_in_cart.id, addOn_id=int(selection[0]), quantity=1)
        return JsonResponse({'item_id': product_in_cart.id, 'price_id': product_in_cart.price.item_id})

    if not add_ons:
        return JsonResponse({'item_id': product_in_cart.id, 'price_id': product_in_cart.price.item_id})

    add_ons.pop('csrfmiddlewaretoken', None)
    add_ons_dict = {add_on: int(value) for add_on, value in add_ons.items() if value != "0"}
    for add_id, qty in add_ons_dict.items():
        Quantity.objects.create(product_id=product_in_cart.id, addOn_id=add_id, quantity=qty)
        # total_add_ons += added.price
    return JsonResponse({'item_id': product_in_cart.id, 'price_id': product_in_cart.price.item_id})


@login_required
def menu_upload(request):
    template = 'uploads/menu.html'
    if request.method == 'POST':
        form = MenuUploadForm(request.POST or None, request.FILES or None)
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
                ingredients = column[4].replace('-', ',')
                if len(ingredients) < 2:
                    ingredients = ''
                # check if item already exists
                menu = Menu.objects.get(id=column[1])
                if not Item.objects.filter(upload_code=column[0], menu=menu):
                    # create item
                    category = Category.objects.get(id=column[2])
                    item, _ = Item.objects.get_or_create(upload_code=column[0], menu=menu, category=category,
                                                         name=column[3], ingredients=ingredients, description=column[5]
                                                         )
                else:
                    # get item
                    item = Item.objects.get(upload_code=column[0], menu=menu)
                    # update item
                    item.__dict__.update(menu__id=column[1], category=column[2], name=column[3],
                                         ingredients=ingredients)
                    item.save()

                item.save()
            return HttpResponseRedirect(reverse('menu:upload-size'))
    form = MenuUploadForm()
    return render(request, template, {'form': form})


@login_required
def size_upload(request):
    template = 'uploads/size.html'
    if request.method == 'POST':
        form = SizeUploadForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            # get form data
            csv_file = form.cleaned_data['csv_file']
            # get csv data
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File must be format:  .CVS')
                print("file error")
                return redirect(reverse('menu:upload-size'))
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            menu_data = csv.reader(io_string, delimiter=",", quotechar="|")
            # create property, address, images
            for column in menu_data:
                # check if item already exists
                item = Item.objects.get(upload_code=column[0])
                size_exists = Price.objects.filter(item=item, size=column[1]).exists()
                if not size_exists:
                    # create price
                    price = Price.objects.create(item=item, size=column[1], price=column[2], price_str=column[3])
                else:
                    # update item
                    size = Price.objects.get(item=item, size=column[1])
                    size.__dict__.update(price=column[2], price_str=column[3])
                    size.save()
                item.save()
            return HttpResponseRedirect(reverse('menu:details', kwargs={'title_slug': item.menu.title_slug}))
    form = MenuUploadForm()
    return render(request, template, {'form': form})


@login_required
def add_ons_upload(request):
    template = 'uploads/add_ons.html'
    if request.method == 'POST':
        form = SizeUploadForm(request.POST or None, request.FILES or None)
        print(form.is_valid())
        if form.is_valid():
            # get form data
            csv_file = form.cleaned_data['csv_file']
            # get csv data
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File must be format:  .CVS')
                print("file error")
                return redirect(reverse('menu:upload-add_ons'))
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            menu_data = csv.reader(io_string, delimiter=",", quotechar="|")
            # create property, address, images
            for column in menu_data:
                # check if item already exists
                codes_list = column[4].split("-")
                items_list = Item.objects.filter(upload_code__in=codes_list)
                products_id = Price.objects.filter(item__in=items_list, size=column[3]).values_list('id', flat=True)
                add_on = AddsOn.objects.create(name=column[0], price=column[1], price_str=column[2])
                for product_id in products_id:
                    add_on.product.add(product_id)
                add_on.save()
            return HttpResponse("Add ons added! all Done")
    form = MenuUploadForm()
    return render(request, template, {'form': form})
