from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
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
    template_name = "menus/details.html"


class MenuDetails(DetailView):
    """View Menu with items"""
    model = Menu
    template_name = "menus/details.html"

    def get_context_data(self, **kwargs):
        """get categories in the context data"""
        context = super().get_context_data(**kwargs)
        context['categories'] = [item.category.name for item in self.object.items.all().distinct('category__name')]
        context['items'] = []
        for category in context['categories']:
            context['items'].append([item for item in self.object.items.filter(category__name=category)])
        return context


def item_prices_get(request, item_id):
    """get all the prices for a item """
    command = request.POST['command']
    if int(command) < 0:
        keys = request.session['cart'].keys()
        prices = [price for price in Price.objects.filter(item__id=item_id, id__in=keys)]
        message = _("Which size would you like to remove?")
    else:
        prices = [price for price in Price.objects.filter(item__id=item_id)]
        message = _("How hungry are you?")
    prices_dict = {}
    for price in prices:
        prices_dict[price.id] = price.size + " " + price.price_str
    return JsonResponse({'list': prices_dict, 'msg': message})
