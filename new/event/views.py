import math
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import Event, EventMember, Cost
from user.models import MyUser
from account.models import Account
from polls.models import Question
from jamah.models import JamahMember, Jamah
from polls.forms import QuestionCreateForm
from .forms import EventCreateForm, CostCreateForm, UserAddForm


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
    left_jamah_members = JamahMember.objects.filter(jamah=event.jamah).exclude(
        member__in = event.members.all()
    )
    users_to_add = []
    for left in left_jamah_members:
        users_to_add.append(left.member)

    template = loader.get_template('event/detail.html')
    eventmembers = EventMember.objects.filter(event=event)

    current_eventmember = EventMember.objects.get(event=event, member=request.user)
    # print(current_eventmember)
    polls = event.polls.all()
    costs = event.cost_set.all()
    pollform = QuestionCreateForm()
    costform = CostCreateForm()
    userform = UserAddForm()
    # todo use forms.py for this
    # userform.fields['choice'].choices = users_to_add
    context = {
        'costs': costs,
        # 'userform': userform,
        'current_eventmember': current_eventmember,
        'eventmembers': eventmembers,
        'pollForm': pollform,
        'costform': costform,
        'polls': polls,
        'event': event,
        'users': users_to_add,
    }
    return HttpResponse(template.render(context, request))

def cost_detail(request, event_id, cost_id):
    cost = Cost.objects.get(pk = cost_id)
    event = cost.event
    eventmember = EventMember.objects.get(event=event, member=request.user)
    template = loader.get_template('event/cost_detail.html')
    cost_transaction_ins = cost.cost_transaction_ins.all()
    recieved = 0
    donation = 0
    for transaction in cost_transaction_ins:
        if transaction.is_donation:
            donation += transaction.amount
        recieved += transaction.amount
    context = {
        'cost_transaction_ins': cost_transaction_ins,
        'donation': donation,
        'recieved': recieved,
        'current_eventmember': eventmember,
        'cost': cost
    }
    print(eventmember)
    return HttpResponse(template.render(context, request))

def create_event_cost(request, event_id):
    event = Event.objects.get(pk = event_id)
    name = request.POST['name']
    amount = request.POST['amount']
    eventmember = EventMember.objects.filter(event=event).filter(member=request.user)[:1]
    eventmembers = event.eventmember_set.all()
    # print(type(amount))
    per_head_cost = math.ceil(float(amount)/eventmembers.count())
    cost = Cost(amount=amount, name=name, added_by=eventmember[0], per_head_cost=per_head_cost, event=event)
    cost.save()
    for event_member in eventmembers:
        cost.cost_bearer.add(event_member)
    cost.save()
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))

def save_member(request, event_id):
    event = Event.objects.get(pk = event_id)
    values = request.POST.getlist('member')
    for value in values:
        user = MyUser.objects.get(pk = value)
        eventmember = EventMember.objects.filter(member=user).filter(event=event)
        # print(eventmember)
        # print(user)
        # check if member is already in the event
        if not eventmember.count():
            event.members.add(user)
            account = Account()
            account.save()
            eventMember = EventMember(member=user, event=event, account=account).save()
        else:
            messages.warning(request, 'The member is already in the event')
    event.save()
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))

def remove_member(request, event_id, member_id):
    event = Event.objects.get(pk = event_id)
    member = MyUser.objects.get(pk = member_id)
    eventmember = EventMember.objects.get(event=event, member=member)
    eventmember.account.delete()
    eventmember.delete()
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
