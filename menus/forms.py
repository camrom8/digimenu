from django import forms
from django.forms import inlineformset_factory

from menus.models import Menu, Item, Category, Establishment, Price

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


class ItemForm(forms.ModelForm):
    """Form for creating and editing item"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"

        self.fields['photo'].widget.attrs['class'] = "custom-file-input"
        self.fields['menu'].empty_label = gettext('Select menu')
        self.fields['category'].empty_label = gettext('Select category')
        self.fields['ingredients'].widget.attrs['placeholder'] = gettext('optional')
        self.fields['description'].widget.attrs['placeholder'] = gettext('optional')
        self.fields['ingredients'].required = False
        self.fields['description'].required = False
    class Meta:
        model = Item
        fields = ['menu', 'category', 'name',
                  'ingredients', 'description', 'photo',
                  ]


class CategoryForm(forms.ModelForm):
    """Form for creating and editing category"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"

    class Meta:
        model = Category
        fields = ['name', ]


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
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"

    class Meta:
        model = Price
        widgets = {
            'price': forms.HiddenInput(),
        }
        fields = ['price', 'price_str', 'size', ]


ItemPriceFormSet = inlineformset_factory(Item,
                                         Price,
                                         form=PriceForm,
                                         extra=1
                                         )

