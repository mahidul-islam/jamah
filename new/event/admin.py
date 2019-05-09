from django.contrib import admin
from .models import Event, Account, TransactionIn, TransactionOut

class TransactionInInline(admin.TabularInline):
    model = TransactionIn
    extra = 1

class TransactionOutInline(admin.TabularInline):
    model = TransactionOut
    extra = 1

class AccountAdmin(admin.ModelAdmin):

    inlines = [TransactionInInline, TransactionOutInline]

admin.site.register(Event)
admin.site.register(Account, AccountAdmin)
