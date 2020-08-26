from django import forms


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)