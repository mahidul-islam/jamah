from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import Event, Account, EventMember
from django.urls import reverse
from user.models import MyUser
from django.contrib import messages
from .forms import EventCreateForm
from polls.forms import QuestionCreateForm
from polls.models import Question


def index(request):
    template = loader.get_template('event/index.html')
    if request.user.is_authenticated:
        form = EventCreateForm()
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
    users_to_add = event.jamah.members.all()
    template = loader.get_template('event/detail.html')
    eventmembers = EventMember.objects.filter(event=event)
    print(eventmembers)
    polls = event.polls.all()
    form = QuestionCreateForm()
    context = {
        'eventmembers': eventmembers,
        'pollForm': form,
        'polls': polls,
        'event': event,
        'users': users_to_add,
    }
    return HttpResponse(template.render(context, request))

# def create(request):
#     name = request.POST['name']
#     account = Account()
#     account.save()
#     event = Event(name = name, creator = request.user, account = account)
#     event.save()
#     event.members.add(request.user)
#     event.save()
#     eventMember = EventMember(member=request.user, event=event, status='creator').save()
#     print(eventMember)
#     return HttpResponseRedirect(reverse('event:index'))

def save_member(request, event_id):
    event = Event.objects.get(pk = event_id)
    values = request.POST.getlist('member')
    for value in values:
        user = MyUser.objects.get(pk = value)
        eventmember = EventMember.objects.filter(member=user).filter(event=event)
        print(eventmember)
        print(user)
        if not eventmember.count():
            event.members.add(user)
            eventMember = EventMember(member=user, event=event).save()
        else:
            messages.warning(request, 'The member is already in the event')
            # return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))
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

def donate(request, event_id):
    template = loader.get_template('event/donate.html')
    context = {}
    return HttpResponse(template.render(context, request))

def pay(request, event_id):
    template = loader.get_template('event/pay.html')
    context = {}
    return HttpResponse(template.render(context, request))
