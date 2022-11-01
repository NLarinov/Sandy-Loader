from django import forms


class NameForm(forms.Form):
    your_link = forms.CharField(max_length=100)
