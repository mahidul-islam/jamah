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
from account.forms import TransactionForm
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
    try:
        current_eventmember = EventMember.objects.get(event=event, member=request.user)
    except:
        messages.info(request, 'You are not a member of the event')
        return HttpResponseRedirect(reverse('jamah:detail', args = (event.jamah.id,)))
    else:
        polls = event.polls.all()
        costs = event.cost_set.all()
        pollform = QuestionCreateForm()
        costform = CostCreateForm()
        userform = UserAddForm()
        transaction_form = TransactionForm()
        transactions = event.account.transaction_ins.all()
        # todo use forms.py for this
        # userform.fields['choice'].choices = users_to_add
        context = {
            'costs': costs,
            'transactions': transactions,
            'transaction_form': transaction_form,
            'current_eventmember': current_eventmember,
            'eventmembers': eventmembers,
            'pollForm': pollform,
            'costform': costform,
            'polls': polls,
            'event': event,
            'users': users_to_add,
        }
        return HttpResponse(template.render(context, request))

def create_cost(request, event_id):
    event = Event.objects.get(pk = event_id)
    name = request.POST['name']
    amount = request.POST['amount']
    eventmember = EventMember.objects.get(event=event, member=request.user)
    cost = Cost(amount=amount, name=name, added_by=eventmember, event=event)
    cost.save()
    event.total_cost = float(event.total_cost) + float(cost.amount)
    event.save()
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))

def delete_cost(request, event_id, cost_id):
    event = Event.objects.get(pk = event_id)
    cost = Cost.objects.get(pk = cost_id)
    event.total_cost = float(event.total_cost) - float(cost.amount)
    cost.delete()
    event.save()
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
            event.per_head_cost = (float(event.total_cost)/event.members.count())
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

def promote_member(request, event_id, member_id):
    event = Event.objects.get(pk = event_id)
    member = MyUser.objects.get(pk = member_id)
    eventmember = EventMember.objects.get(event=event, member=member)
    if eventmember.status == 'member':
        eventmember.status = 'admin'
    elif eventmember.status == 'admin':
        eventmember.status = 'modarator'
    eventmember.save()
    # print(event.members.all())
    messages.success(request, 'You have Promoted a member !!!')
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))

def demote_member(request, event_id, member_id):
    event = Event.objects.get(pk = event_id)
    member = MyUser.objects.get(pk = member_id)
    eventmember = EventMember.objects.get(event=event, member=member)
    if eventmember.status == 'modarator':
        eventmember.status = 'admin'
    elif eventmember.status == 'admin':
        eventmember.status = 'member'
    eventmember.save()
    # print(event.members.all())
    messages.success(request, 'You have Demoted a member !!!')
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

def make_transaction(request, event_id):
    event = Event.objects.get(pk = event_id)
    transaction_form = TransactionForm()
    context = {
        'event': event,
        'transaction_form': transaction_form
    }
    template = loader.get_template('event/transaction.html')
    return HttpResponse(template.render(context, request))

def transact(request, event_id):
    messages.success(request, "This is where the transaction will be complete...")
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))
