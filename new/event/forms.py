from django import forms

class EventCreateForm(forms.Form):
    name = forms.CharField(max_length=200)
