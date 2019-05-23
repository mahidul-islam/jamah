from django import forms

class EventCreateForm(forms.Form):
    name = forms.CharField(max_length=200)

class CostCreateForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    name = forms.CharField(max_length=255)

class TransactionInForm(forms.Form):
    pass

class UserAddForm(forms.Form):
    choice = forms.MultipleChoiceField(queryset = None ,widget=forms.CheckBoxSelectMultiple)
