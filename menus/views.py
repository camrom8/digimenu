from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.generic import CreateView, ListView, TemplateView, DetailView

from menus.forms import MenuForm, CategoryForm, EstablishmentForm, ItemForm, ItemPriceFormSet
from menus.models import Menu, Item, Category, Establishment, Price
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
    # print(request.session['cart'])
    if int(command) < 0:
        prices = [price for price in Price.objects.filter(item__id=item_id, id__in=keys)]
        message = _("Which size would you like to remove?")
    else:
        if keys:
            key_list = list(keys)
            # check that product belongs to the same menu
            menu = Price.objects.get(id=key_list[0])
            if menu.item.menu != Item.objects.get(id=item_id).menu:
                message = _('All items on plate must belong to the same menu')
                text = _('Send your order or clear your plate before adding this item')
                return JsonResponse({'list': -1, 'msg': message, 'text': text})

        prices = [price for price in Price.objects.filter(item__id=item_id)]
        message = _("How hungry are you?")

    prices_dict = {}
    if len(prices) == 1:
        return JsonResponse({'id': str(prices[0].id)})
    for price in prices:
        prices_dict[price.id] = _(price.size) + " " + price.price_str

    return JsonResponse({'list': prices_dict, 'msg': message})
