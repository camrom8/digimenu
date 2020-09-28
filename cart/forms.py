from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext

from menus.helpers.functions import to_currency

CHOICES_TIP = [(i, to_currency(i)) for i in range(0, 20000, 1000)]
CHOICES_TIP_PERCENT = [(i, str(i) + "%") for i in range(0, 25, 5)]


class DetailsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = _('optional field')
        self.fields['address'].widget.attrs['placeholder'] = _('optional field')
        self.fields['comments'].widget.attrs['placeholder'] = _('optional field')
        self.fields['name'].widget.attrs['class'] = "form-control"
        self.fields['address'].widget.attrs['class'] = "form-control"
        self.fields['comments'].widget.attrs['class'] = "form-control"
        self.fields['tip'].widget.attrs['class'] = "form-control"
        self.fields['tip_percent'].widget.attrs['class'] = "form-control"

    name = forms.CharField(max_length=40, required=False, label=_('name'))
    address = forms.CharField(max_length=90, required=False, label=_('address or table'), )
    comments = forms.CharField(max_length=90, required=False, label=_('comments'))
    pickup = forms.ChoiceField(choices={('RECOGE', _('Restaurant')),
                                        ('DOMICILIO', _('delivery'))},
                               label=_('Delivery'),
                               widget=forms.RadioSelect)
    tip = forms.CharField(max_length=7)
    tip_percent = forms.ChoiceField(choices=CHOICES_TIP_PERCENT, label=_('tip'))
    tip_number = forms.CharField(max_length=7, widget=forms.HiddenInput)
