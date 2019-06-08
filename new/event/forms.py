from django import forms

class EventCreateForm(forms.Form):
    name = forms.CharField(max_length=200)

class CostCreateForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    name = forms.CharField(max_length=255)
    from_accountant_or_myself = forms.ModelChoiceField(queryset=None)

class UserAddForm(forms.Form):
    candidate_members = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

class SelectHeadAccountantForm(forms.Form):
    head_accountant = forms.ModelChoiceField(queryset=None)
