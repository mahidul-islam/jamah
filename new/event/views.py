from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import Event, Account
from django.urls import reverse
from user.models import MyUser
from django.contrib import messages
from .forms import EeventCreateForm
from polls.forms import QuestionCreateForm
from polls.models import Question


def index(request):
    template = loader.get_template('event/index.html')
    if request.user:
        form = EeventCreateForm()
        eventbyme = Event.objects.filter(creator = request.user)
        eventbyall = request.user.event_set.all()
        context = {
            'form':form,
            'eventOfMine':eventbyme,
            'eventbyall':eventbyall
        }
        return HttpResponse(template.render(context, request))

    else:
        context = {}
        messages.success(request, 'Please Log in to use this feature')
        return HttpResponse(template.render(context, request))

def detail(request, event_id):
    event = Event.objects.get(pk = event_id)
    users = MyUser.objects.all()
    template = loader.get_template('event/detail.html')
    eventmembers = event.members.all()
    polls = event.question_set.all()
    form = QuestionCreateForm()
    context = {
        'pollForm': form,
        'polls': polls,
        'event': event,
        'users': users,
    }
    return HttpResponse(template.render(context, request))

def create(request):
    name = request.POST['name']
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

def create_event_poll(request, event_id):
    event = Event.objects.get(pk = event_id)
    question_text = request.POST['question_text']
    poll = Question(question_text=question_text, creator=request.user, event=event).save()
    messages.success(request, 'Added a Poll for the event...')
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))
