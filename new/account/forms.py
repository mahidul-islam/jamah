from django import forms


class TransactionForm(forms.Form):
    is_donation = forms.BooleanField()
    amount = forms.DecimalField(max_digits = 10, decimal_places = 2)
