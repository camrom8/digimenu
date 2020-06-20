from django import forms

from menus.models import Establishment


class SearchBarForm(forms.Form):
    """Index main search bar form inputs"""
    city = forms.CharField(max_length=127, required=False)
    establishments = forms.ModelChoiceField(queryset=Establishment.objects.all(), empty_label="Todo tipo")
