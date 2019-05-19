from django import forms
from .models import Question, Choice, Comment, Vote


class QuestionCreateForm(forms.Form):
    question_text = forms.CharField(max_length=200)

# TODO: use vote create form
class VoteCreateForm(forms.Form):
    choice = forms.ModelChoiceField(queryset = None ,widget=forms.RadioSelect)

class ChoiceCreateForm(forms.Form):
    choice_text = forms.CharField(max_length=200)

class CommentCreateForm(forms.Form):
    comment_text = forms.CharField(max_length=200)
