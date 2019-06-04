from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from .forms import MyUserCreationForm
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import MyUser, UserInfo
from account.models import Account


def add_account(request):
    account = Account(description=request.user.username + '\'s account')
    account.save()
    print(account.description)
    userinfo = UserInfo(user=request.user, account=account)
    userinfo.save()
    return HttpResponseRedirect(reverse('home'))

def SignUp(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        # print(form.is_valid())
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('myuser:add_account'))
    else:
        # print('method is not Post')
        form = MyUserCreationForm()

    template = loader.get_template('registration/signup.html')
    return HttpResponse(template.render({'form':form}, request))


# made by me
# def SignUp(request):
#     if request.method == 'POST':
#         print('Method is POST')
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             print('form is valid')
#             form.save()
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             user = authenticate(username = username, password = password)
#             login(request, user)
#             print(user)
#             return HttpResponseRedirect(reverse('home'))
#         else:
#             template = loader.get_template('registration/signup.html')
#             context = { 'form':form }
#             return HttpResponse(template.render(context, request))
#     else:
#         form = UserCreationForm()
#         template = loader.get_template('registration/signup.html')
#         context = {'form': form}
#         return HttpResponse(template.render(context, request))
