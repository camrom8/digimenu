from django import forms
from django.utils.translation import gettext_lazy as _


class DetailsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].widget.attrs['placeholder'] = _('Type Address or table number')
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"

    name = forms.CharField(max_length=40, required=False, label=_('name'))
    address = forms.CharField(max_length=90, required=False, label=_('address or table'), )
    pickup = forms.BooleanField(initial=False, label=_('pick up'), required=False)
    comments = forms.CharField(max_length=90, required=False, label=_('comments'))
