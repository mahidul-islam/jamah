from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import Event, Account
from django.urls import reverse

def index(request):
    template = loader.get_template('event/index.html')
    try:
        events = Event.objects.filter(creator = request.user)
        eventss = Event.objects.filter(creator = request.user)
    except:
        context = {'message': "Please Log in to use this feature"}
        return HttpResponse(template.render(context, request))
    else:
        context = {
            'eventOfMine':events,
            'eventOfOthers':eventss
        }
        return HttpResponse(template.render(context, request))

def detail(request, event_id):
    event = Event.objects.get(pk = event_id)
    template = loader.get_template('event/detail.html')
    context = { 'event': event }
    return HttpResponse(template.render(context, request))

def create(request):
    name = request.POST['event']
    # print('one')
    account = Account()
    account.save()
    # print(account)
    Event(name = name, creator = request.user, account = account).save()

    return HttpResponseRedirect(reverse('event:index'))
