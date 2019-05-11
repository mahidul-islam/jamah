from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from user.models import MyUser
from django.template import loader
from polls.models import Question


def profile(request, user_id):
    try:
        user = MyUser.objects.get(pk = user_id)
        events = user.event_set.all()
        polls = user.question_set.all()
        context = {
            'polls': polls,
            'events': events,
            'user': user,
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
