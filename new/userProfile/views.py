from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from user.models import MyUser
from django.template import loader


def profile(request, user_id):
    try:
        user = MyUser.objects.get(pk = user_id)
        context = {
            'user': user,
            'error_message':'no error'
        }
    except:
        user = False
        context = {
            'error_message': 'user not found',
            'user': user
        }
        template = loader.get_template('userProfile/profile.html')
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('userProfile/profile.html')
        return HttpResponse(template.render(context, request))

def alluser(request):
    users = MyUser.objects.all()
    return HttpResponse('This is all user')
