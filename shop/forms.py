from django import forms
from .models import Color

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(-1, 21)]


class CartAddProduct(forms.Form):

    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label='Cantidad')
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
