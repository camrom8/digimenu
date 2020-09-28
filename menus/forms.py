from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from menus.models import Menu, Item, Category, Establishment, Price, MenuAdvertising

from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext


class MenuForm(forms.ModelForm):
    """Form for creating and editing menu"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"
        self.fields['description'].widget.attrs.update(rows='4')

    class Meta:
        model = Menu
        fields = ['owner', 'establishment', 'title', 'subtitle', 'description', 'logo']


class AdForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"

    class Meta:
        model = MenuAdvertising
        fields = ['title', 'description', 'photo']


class ItemForm(forms.ModelForm):
    """Form for creating and editing item"""

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner')
        menu = kwargs.pop('menu')
        category = kwargs.pop('category')
        super().__init__(*args, **kwargs)
        if category:
            self.fields['category'] = forms.ModelChoiceField(queryset=Category.objects.filter(id=category.id),
                                                             empty_label=None)
            self.fields['category'].widget.attrs['readonly'] = True
        else:
            self.fields['category'] = forms.ModelChoiceField(queryset=Category.objects.filter(owner=owner))
            self.fields['category'].empty_label = gettext('Select category')
        if menu:
            self.fields['menu'] = forms.ModelChoiceField(queryset=Menu.objects.filter(id=menu.id),
                                                             empty_label=None)
            self.fields['menu'].widget.attrs['readonly'] = True
        else:
            self.fields['menu'] = forms.ModelChoiceField(queryset=Menu.objects.filter(owner=owner))
            self.fields['menu'].empty_label = gettext('Select menu')
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"

        self.fields['category'].initial = category
        self.fields['category'].label = _('category')
        self.fields['photo'].widget.attrs['class'] = "custom-file-input"
        self.fields['menu'].initial = menu
        self.fields['name'].label = _('name')
        self.fields['ingredients'].widget.attrs['placeholder'] = gettext('optional')
        self.fields['ingredients'].label = _('description')
        self.fields['notes'].widget.attrs['placeholder'] = gettext('informacion extra. optional')
        self.fields['notes'].label = _('notas')
        self.fields['ingredients'].required = False
        self.fields['notes'].required = False

    class Meta:
        model = Item
        fields = ['menu', 'category', 'name',
                  'ingredients', 'notes', 'photo',
                  ]


class CategoryForm(forms.ModelForm):
    """Form for creating and editing category"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"
        self.fields['name'].label = _('name')

    class Meta:
        model = Category
        fields = ['name', 'position']


class EstablishmentForm(forms.ModelForm):
    """Form for creating and editing category"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"

    class Meta:
        model = Establishment
        fields = ['type', ]


class PriceForm(forms.ModelForm):
    """Form for creating price """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['size'].label = _('size')
        self.fields['price_str'].label = _('price')
        self.fields['price_str'].required = True
        self.fields['price_str'].widget.attrs['class'] = "form-control input-price"
        self.fields['size'].widget.attrs['class'] = "form-control input-price"
    price = forms.DecimalField(widget=forms.HiddenInput)

    class Meta:
        model = Price
        fields = ['price', 'price_str', 'size']


ItemPriceFormSet = inlineformset_factory(Item,
                                         Price,
                                         form=PriceForm,
                                         extra=1
                                         )

ItemPriceFormSet2 = inlineformset_factory(Item,
                                          Price,
                                          form=PriceForm,
                                          extra=0,
                                          can_delete=True,
                                          )

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(-1, 21)]


class CartAddProduct(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label='Cantidad')
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)


class MenuUploadForm(forms.Form):
    csv_file = forms.FileField(label=_('csv file'))


class SizeUploadForm(forms.Form):
    csv_file = forms.FileField(label=_('csv file'))

