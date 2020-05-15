from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Nombre'
        self.fields['last_name'].label = 'Apellido'
        self.fields['last_name'].label = 'Apellido'
        self.fields['phone'].label = 'Telefono'
        self.fields['address'].label = 'Dirección'
        self.fields['send'].label = 'Enviar a domilio ($2000)'

        self.fields['address'].widget.attrs.update(placeholder='Dirección para la entrega', required=False)
        self.fields['email'].widget.attrs.update(required=False)

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'send', 'address',
                  ]
