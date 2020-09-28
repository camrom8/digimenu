import csv
import io
import unidecode
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, TemplateView, DetailView, UpdateView, DeleteView

from cart.cart import Cart
from menus.forms import MenuForm, CategoryForm, EstablishmentForm, ItemForm, ItemPriceFormSet, MenuUploadForm, \
    SizeUploadForm, ItemPriceFormSet2, AdForm
from menus.models import Menu, Item, Category, Establishment, Price, AddsOn, ProductInCart, Quantity, MenuAnalytic, \
    MenuAdvertising
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
    template_name = "chunks/item_crud.html"
    success_url = reverse_lazy('menu:item-create')

    def get(self, request, *args, **kwargs):
        try:
            self.category = Category.objects.get(id=request.GET['category_id'])
        except:
            self.category = ""
        try:
            self.menu = Menu.objects.get(id=request.GET['menu_id'])
        except:
            self.menu = ""
        return super(ItemCreate, self).get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            self.category = Category.objects.get(id=request.POST['category_id'])
        except:
            self.category = ""
        try:
            self.menu = Menu.objects.get(id=request.POST['menu_id'])
        except:
            self.menu = ""
        return super(ItemCreate, self).post(self, request, *args, **kwargs)

    def form_valid(self, form):
        """valid the other 2 forms, location and property details"""
        context = self.get_context_data()
        prices = context['price']
        if prices.is_valid():
            item = form.save()
            prices.instance = item
            prices.save()
            return render(self.request, 'chunks/item_display.html', {'item': item,
                                                                     'list': [0, item.category.id],
                                                                     'edit': False})
        return super(ItemCreate, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        """Add price inline form"""
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['price'] = ItemPriceFormSet(self.request.POST)
            context['cat_id'] = self.category.id
        else:
            context['price'] = ItemPriceFormSet()
            context['cat_id'] = self.category.id

        return context

    def get_form_kwargs(self):
        kwargs = super(ItemCreate, self).get_form_kwargs()
        kwargs['owner'] = self.menu.owner
        kwargs['menu'] = self.menu
        kwargs['category'] = self.category
        return kwargs


class ItemUpdate(UpdateView):
    """View to create Item"""
    model = Item
    form_class = ItemForm
    template_name = "chunks/item_crud.html"
    success_url = reverse_lazy('menu:upload')

    def get(self, request, *args, **kwargs):
        try:
            self.category = Category.objects.get(id=request.GET['category_id'])
        except:
            self.category = ""
        try:
            self.menu = Menu.objects.get(id=request.GET['menu_id'])
        except:
            self.menu = ""
        return super(ItemUpdate, self).get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            self.category = Category.objects.get(id=request.POST['category_id'])
        except:
            self.category = ""
        try:
            self.menu = Menu.objects.get(id=request.POST['menu_id'])
        except:
            self.menu = ""
        return super(ItemUpdate, self).post(self, request, *args, **kwargs)

    def form_valid(self, form):
        """valid the other 2 forms, location and property details"""
        context = self.get_context_data()
        prices_form = context['price']
        if prices_form.is_valid():
            item = form.save()
            prices_form.save()
            return render(self.request, 'chunks/item_display.html', {'item': item,
                                                                     'list': [0, item.category.id],
                                                                     'edit': True})
        return super(ItemUpdate, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        """Add price inline form"""
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['price'] = ItemPriceFormSet2(self.request.POST, instance=self.object)
            context['cat_id'] = self.category.id
            context['item_id'] = self.object.id
        else:
            context['price'] = ItemPriceFormSet2(instance=self.object)
            context['cat_id'] = self.category.id
            context['item_id'] = self.object.id

        return context

    def get_form_kwargs(self):
        kwargs = super(ItemUpdate, self).get_form_kwargs()
        kwargs['owner'] = self.menu.owner
        kwargs['menu'] = self.menu
        kwargs['category'] = self.category
        return kwargs


class ItemDelete(DeleteView):
    model = Item

    def delete(self, request, *args, **kwargs):
        item = self.get_object()
        item_id = item.id
        item.delete()
        if Category.objects.filter(id=item_id).exists():
            return JsonResponse({'msg': 'error. por favor intentelo de nuevo'})
        else:
            divId = '#div-item' + str(item_id)
            return JsonResponse({'id': divId})


class CategoryCreate(CreateView):
    """View to create Category"""
    model = Category
    form_class = CategoryForm
    template_name = "chunks/category_crud.html"
    success_url = reverse_lazy('menu:edit')

    def post(self, request, *args, **kwargs):
        self.menu = Menu.objects.get(id=request.POST['menu_id'])
        self.owner = get_user_model().objects.get(id=request.POST['menu_owner'])
        return super(CategoryCreate, self).post(self, request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.menu.owner
        self.object.menu = self.menu
        self.object.save()
        return redirect(reverse('menu:edit-partial', kwargs={'title_slug': self.menu.title_slug, 'partial': 1}))


class CategoryUpdate(UpdateView):
    """View to create Category"""
    model = Category
    form_class = CategoryForm
    template_name = "chunks/category_crud.html"

    def post(self, request, *args, **kwargs):
        self.menu = Menu.objects.get(id=request.POST['menu_id'])
        return super(CategoryUpdate, self).post(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """pass id to template"""
        context = super().get_context_data(**kwargs)
        context['id'] = self.object.id
        return context

    def form_valid(self, form):
        position = Category.objects.get(id=self.object.id).position
        if position != form.cleaned_data['position']:
            self.object = form.save()
            return redirect(reverse('menu:edit-partial', kwargs={'title_slug': self.menu.title_slug, 'partial': 1}))
        self.object = form.save()
        divId = '#cat' + str(self.object.id)
        return JsonResponse({'id': divId, 'name': self.object.name})


class CategoryDelete(DeleteView):
    model = Category

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        cat_id = category.id
        # cat_name = category.name
        category.delete()
        if Category.objects.filter(id=cat_id).exists():
            return JsonResponse({'msg': 'error. por favor intentelo de nuevo'})
        else:
            divId = '.cat-' + str(cat_id)
            return JsonResponse({'id': divId})


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
        map_url2 = ""
        if "iPhone" in request.META['HTTP_USER_AGENT'] or "iPad" in request.META['HTTP_USER_AGENT']:
            map_url = f'https://www.google.com/maps/search/?api=1&query={str(self.object.lat)},{str(self.object.lng)}&query_place_id={self.object.subtitle}'
            map_url2 = f'href="http://maps.apple.com/maps?saddr=Current%20Location&daddr={str(self.object.lat)},{str(self.object.lng)}'
        else:
            map_url = f'https://www.google.com/maps/search/?api=1&query={str(self.object.lat)},{str(self.object.lng)}&query_place_id={self.object.subtitle}'
        context['map_url'] = map_url
        if map_url2:
            context['map_url2'] = map_url2
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        """get categories in the context data"""
        context = super().get_context_data(**kwargs)
        categories = self.object.categories.all()
        ads = self.object.ads.all()
        context['ads'] = ads
        context['items'] = {}
        for category in categories:
            context['items'][category.name] = str(category.id)
            # [item for item in self.object.items.filter(category=category).order_by('upload_code', 'name')]
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

    def get(self, request, *args, **kwargs):
        print(request.user.is_superuser)
        if request.user != self.get_object().owner and not request.user.is_superuser:
            return redirect(reverse_lazy('account:login'))
        self.partial = self.kwargs.get('partial', None)
        return super(MenuEditDetails, self).get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """get categories in the context data"""
        context = super().get_context_data(**kwargs)
        categories = self.object.categories.all()
        ads = self.object.ads.all()
        context['ads'] = ads
        context['items'] = {}
        for category in categories:
            context['items'][category.name] = \
                [[item for item in self.object.items.filter(category=category).order_by('upload_code', 'name')],
                 category.id]
        return context

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        template_name = self.get_template_names()
        if self.partial:
            template_name = "chunks/edit_menu.html"
        return self.response_class(
            request=self.request,
            template=template_name,
            context=context,
            using=self.template_engine,
            **response_kwargs
        )


class AdUpdate(UpdateView):
    model = MenuAdvertising
    form_class = AdForm
    template_name = "chunks/ad_crud.html"

    def get_context_data(self, **kwargs):
        """pass id to template"""
        context = super().get_context_data(**kwargs)
        context['id'] = self.object.id
        return context

    def form_valid(self, form):
        """valid the other 2 forms, location and property details"""
        ad = form.save()
        ads = self.model.objects.filter(menu=ad.menu)
        return render(self.request, 'chunks/carousel_ads.html', {'ads': ads})


@csrf_exempt
def get_category_items(request, cat_id):
    """render list of items for a category"""
    items = Item.objects.filter(category_id=cat_id)
    cart = Cart(request)
    itemsQty = {}
    for item in cart:
        itemsQty[str(item['product'].price.item.id)] = item['quantity']
    return render(request, "chunks/items_in_cat.html", {'items': items, 'itemsQty': itemsQty})


@csrf_exempt
def menu_access_count(request):
    menu_id = int(request.POST['menu_id'])
    analitics, _ = MenuAnalytic.objects.get_or_create(menu_id=menu_id)
    analitics.visit += 1
    analitics.save()
    return JsonResponse({'msg': 1})


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
                                                         name=column[3], ingredients=ingredients, notes=column[5]
                                                         )
                else:
                    # get item
                    item = Item.objects.get(upload_code=column[0], menu=menu)
                    # update item
                    item.__dict__.update(menu__id=column[1], category=column[2], name=column[3],
                                         ingredients=ingredients, notes=column[5])
                    item.save()

                item.save()
            return HttpResponseRedirect(reverse('menu:upload-size'))
    if not request.user.is_superuser:
        return redirect(reverse_lazy('account:login'))
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
    if not request.user.is_superuser:
        return redirect(reverse_lazy('account:login'))
    form = MenuUploadForm()
    return render(request, template, {'form': form})


@login_required
def add_ons_upload(request):
    template = 'uploads/add_ons.html'
    if request.method == 'POST':
        form = SizeUploadForm(request.POST or None, request.FILES or None)
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
    if not request.user.is_superuser:
        return redirect(reverse_lazy('account:login'))
    form = MenuUploadForm()
    return render(request, template, {'form': form})
