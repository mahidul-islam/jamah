from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import Event, Account
from django.urls import reverse
from user.models import MyUser


def index(request):
    template = loader.get_template('event/index.html')
    try:
        eventbyme = Event.objects.filter(creator = request.user)
        eventbyall = request.user.event_set.all()
    except:
        context = {'message': "Please Log in to use this feature"}
        return HttpResponse(template.render(context, request))
    else:
        context = {
            'eventOfMine':eventbyme,
            'eventbyall':eventbyall
        }
        return HttpResponse(template.render(context, request))

def detail(request, event_id):
    event = Event.objects.get(pk = event_id)
    users = MyUser.objects.all()
    template = loader.get_template('event/detail.html')
    eventmembers = event.members.all()
    context = {
        'event': event,
        'users': users,
        'eventmembers': eventmembers
    }
    return HttpResponse(template.render(context, request))

def create(request):
    name = request.POST['event']
    account = Account()
    account.save()
    event = Event(name = name, creator = request.user, account = account)
    event.save()
    event.members.add(request.user)
    event.save()
    return HttpResponseRedirect(reverse('event:index'))

def save_member(request, event_id):
    event = Event.objects.get(pk = event_id)
    values = request.POST.getlist('member')
    for value in values:
        user = MyUser.objects.get(pk = value)
        event.members.add(user)
        print(user)
    event.save()
    # print(event.members.all())
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))

def remove_member(request, event_id, member_id):
    event = Event.objects.get(pk = event_id)
    member = MyUser.objects.get(pk = member_id)
    event.members.remove(member)
    event.save()
    # print(event.members.all())
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))
