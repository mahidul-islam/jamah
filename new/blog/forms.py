from django import forms
from .models import Blog

# class CreateBlogForm(forms.Form):
#     heading = forms.CharField(label='Heading', max_length=200)
#     body = forms.CharField(widget=forms.Textarea)
#     is_finished = forms.BooleanField(label='Finished?')
#     is_published = forms.BooleanField(label='Publish?')

class CreateBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['heading_text', 'body_text', 'is_finished', 'is_published']
        widget = {
            'body_text': forms.Textarea(),
        }
