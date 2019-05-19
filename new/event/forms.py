from django import forms

class EeventCreateForm(forms.Form):
    name = forms.CharField(max_length=200)
