from django.contrib import admin
from .forms import MyUserChangeForm, MyUserCreationForm
from .models import MyUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model


class UserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = MyUser
    list_display = ['username','email','is_active','is_staff',]

admin.site.register(MyUser, UserAdmin)
