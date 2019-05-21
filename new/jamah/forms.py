from django import forms

class JamahCreateForm(forms.Form):
    jamahname = forms.CharField(max_length=255)
