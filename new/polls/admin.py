from django.contrib import admin
from .models import Question, Choice, Comment, Vote

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 1

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class QuestionAdmin(admin.ModelAdmin):

    inlines = [ChoiceInline, CommentInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Vote)
# admin.site.register(Choice)
