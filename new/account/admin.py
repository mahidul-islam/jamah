from django.contrib import admin
from .models import Account, Transaction


class TransactionOutInline(admin.TabularInline):
    model = Transaction
    fk_name = 'comes_from'
    extra = 0

class TransactionInInline(admin.TabularInline):
    model = Transaction
    fk_name = 'goes_to'
    extra = 0

class AccountAdmin(admin.ModelAdmin):
    inlines = [TransactionInInline, TransactionOutInline]

admin.site.register(Account, AccountAdmin)
