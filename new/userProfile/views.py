from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from user.models import MyUser
from django.template import loader
from polls.models import Question
from django.contrib import messages


def profile(request, user_id):
    try:
        user = MyUser.objects.get(pk = user_id)
        events = user.event_set.all()
        polls = user.question_set.all()
        context = {
            'polls': polls,
            'events': events,
            'user': user
        }
    except:
        context = {
            'user' : False
        }
        messages.warning(request, 'User not Found')
        template = loader.get_template('userProfile/profile.html')
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('userProfile/profile.html')
        return HttpResponse(template.render(context, request))

def alluser(request):
    users = MyUser.objects.all()
    return HttpResponse('This is all user')

def send_mail(request, user_id):
    return HttpResponseRedirect(reverse('profile:user_profile', args = (user_id,)))
