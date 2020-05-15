from django import forms


class SearchBarForm(forms.Form):
    """Index main search bar form inputs"""
    address = forms.CharField(max_length=127, required=False)
    state = forms.CharField(max_length=127, required=False)
    locality = forms.CharField(max_length=127, required=False)
