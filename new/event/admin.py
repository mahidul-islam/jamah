from django.contrib import admin
from .models import Event, Account, TransactionIn, TransactionOut
from polls.models import Question


class TransactionInInline(admin.TabularInline):
    model = TransactionIn
    extra = 1

class TransactionOutInline(admin.TabularInline):
    model = TransactionOut
    extra = 1

class AccountAdmin(admin.ModelAdmin):
    inlines = [TransactionInInline, TransactionOutInline]

class PollsInline(admin.TabularInline):
    model = Question
    extra = 1

class EventAdmin(admin.ModelAdmin):
    inlines = [PollsInline]

admin.site.register(Event, EventAdmin)
admin.site.register(Account, AccountAdmin)
