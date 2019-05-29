import math
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import Event, EventMember, Cost
from user.models import MyUser
from account.models import Account, Transaction
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
    try:
        current_eventmember = EventMember.objects.get(event=event, member=request.user)
    except:
        messages.info(request, 'You are not a member of the event')
        return HttpResponseRedirect(reverse('jamah:detail', args = (event.jamah.id,)))
    else:
        left_jamah_members = JamahMember.objects.filter(jamah=event.jamah).exclude(
            member__in = event.members.all()
        )
        users_to_add = []
        for left in left_jamah_members:
            users_to_add.append(left.member)
        candidate_accountants = EventMember.objects.filter(event=event).exclude(is_accountant=True)
        # print(candidate_accountants)
        template = loader.get_template('event/detail.html')
        eventmembers = EventMember.objects.filter(event=event).order_by('-timestamp')
        polls = event.polls.all()
        costs = event.cost_set.all()
        pollform = QuestionCreateForm()
        costform = CostCreateForm()
        userform = UserAddForm()
        transaction_form = TransactionForm()
        transactions = event.account.transaction_ins.all()
        donations = event.account.transaction_ins.filter(is_donation = True)
        total_donation = 0
        for donation in donations:
            total_donation += donation.amount
        # todo use forms.py for this
        # userform.fields['choice'].choices = users_to_add
        print(users_to_add)
        context = {
            'total_donation': total_donation,
            'candidate_accountants': candidate_accountants,
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

def edit(request, event_id):
    event = Event.objects.get(pk = event_id)
    current_eventmember = EventMember.objects.get(event=event, member=request.user)
    left_jamah_members = JamahMember.objects.filter(jamah=event.jamah).exclude(
        member__in = event.members.all()
    )
    users_to_add = []
    for left in left_jamah_members:
        users_to_add.append(left.member)
    candidate_accountants = EventMember.objects.filter(event=event).exclude(is_accountant=True)
    # print(candidate_accountants)
    eventmembers = EventMember.objects.filter(event=event).order_by('-timestamp')
    polls = event.polls.all()
    costs = event.cost_set.all()
    pollform = QuestionCreateForm()
    costform = CostCreateForm()
    userform = UserAddForm()
    transaction_form = TransactionForm()
    transactions = event.account.transaction_ins.all()
    donations = event.account.transaction_ins.filter(is_donation = True)
    # todo use forms.py for this
    # userform.fields['choice'].choices = users_to_add
    print(users_to_add)
    context = {
        'candidate_accountants': candidate_accountants,
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
    template = loader.get_template('event/edit.html')
    return HttpResponse(template.render(context, request))

def finance(request, event_id):
    event = Event.objects.get(pk = event_id)
    current_eventmember = EventMember.objects.get(event=event, member=request.user)
    costs = event.cost_set.all()
    transactions = event.account.transaction_ins.filter(is_donation = False)
    donations = event.account.transaction_ins.filter(is_donation = True)
    total_donation = 0
    for donation in donations:
        total_donation += donation.amount
    print(total_donation)
    print(transactions)
    context = {
        'total_donation': total_donation,
        'donations': donations,
        'costs': costs,
        'transactions': transactions,
        'current_eventmember': current_eventmember,
        'event': event,
    }
    template = loader.get_template('event/event_finance.html')
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
    messages.success(request, 'The cost is added !!! ')
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))

def delete_cost(request, event_id, cost_id):
    event = Event.objects.get(pk = event_id)
    cost = Cost.objects.get(pk = cost_id)
    event.total_cost = float(event.total_cost) - float(cost.amount)
    cost.delete()
    event.save()
    messages.warning(request, 'The cost is deleted !!! ')
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))

def object_cost(request, event_id, cost_id):
    event = Event.objects.get(pk = event_id)
    eventmember = EventMember.objects.get(event=event, member=request.user)
    cost = Cost.objects.get(pk = cost_id)
    people_objected = cost.objected_by.all()
    if eventmember in people_objected:
        messages.success(request, 'You already objected the COST !!! ')
        return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))
    cost.is_objected = True
    cost.objected_by.add(eventmember)
    cost.save()
    messages.success(request, 'The cost is objected !!! ')
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))

def save_member(request, event_id):
    event = Event.objects.get(pk = event_id)
    values = request.POST.getlist('member')
    for value in values:
        user = MyUser.objects.get(pk = value)
        try:
            eventmember = EventMember.objects.get(member=user, event=event)
        # check if member is already in the event
        except:
            event.members.add(user)
            account = Account()
            account.save()
            event.per_head_cost = (float(event.total_cost)/event.members.count())
            eventMember = EventMember(member=user, event=event, account=account).save()
            messages.success(request, 'The member is added in the event')
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
        messages.success(request, 'You have Promoted a member !!!')
    elif eventmember.status == 'admin':
        eventmember.status = 'modarator'
        messages.success(request, 'You have Promoted a member !!!')
    else:
        messages.warning(request, 'The member could not be promoted !!!')
    eventmember.save()
    # print(event.members.all())
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))

def demote_member(request, event_id, member_id):
    event = Event.objects.get(pk = event_id)
    member = MyUser.objects.get(pk = member_id)
    eventmember = EventMember.objects.get(event=event, member=member)
    if eventmember.status == 'admin':
        eventmember.status = 'member'
        messages.success(request, 'You have Demoted a member !!!')
    elif eventmember.status == 'modarator':
        eventmember.status = 'admin'
        messages.success(request, 'You have Demoted a member !!!')
    else:
        messages.warning(request, 'The member could not be demoted !!!')
    eventmember.save()
    # print(event.members.all())
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))

def add_accountants(request, event_id):
    event = Event.objects.get(pk = event_id)
    values = request.POST.getlist('member')
    for value in values:
        user = MyUser.objects.get(pk = value)
        eventmember = EventMember.objects.get(member=user, event=event)
        eventmember.is_accountant = True
        eventmember.save()
    event.save()
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))

def create_event_poll(request, event_id):
    event = Event.objects.get(pk = event_id)
    question_text = request.POST['question_text']
    poll = Question(question_text=question_text, creator=request.user, event=event).save()
    messages.success(request, 'Added a Poll for the event...')
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))

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
    event = Event.objects.get(pk = event_id)
    is_donation = request.POST.getlist('is_donation')
    amount = request.POST['amount']
    eventmember = EventMember.objects.get(member=request.user, event=event)
    if len(is_donation):
        transaction = Transaction(amount=amount, goes_to=event.account, comes_from=eventmember.account, is_donation=True)
    else:
        transaction = Transaction(amount=amount, goes_to=event.account, comes_from=eventmember.account)
    event.account.amount = float(event.account.amount) + float(amount)
    event.account.save()
    eventmember.account.amount = float(eventmember.account.amount) + float(amount)
    eventmember.account.save()
    transaction.save()
    messages.success(request, 'Added Money To the event with your name')
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))

def verify_transaction(request, event_id, transaction_id):
    event = Event.objects.get(pk = event_id)
    transaction = Transaction.objects.get(pk = transaction_id)
    eventmember = EventMember.objects.get(member=request.user, event=event)
    if eventmember.is_accountant:
        transaction.verified_by = request.user
        transaction.save()
        messages.success(request, 'The transaction is Verified !!!')
    else:
        messages.warning(request, 'You are not Authorized to verify !!!')
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))

def delete_transaction(request, event_id, transaction_id):
    event = Event.objects.get(pk = event_id)
    transaction = Transaction.objects.get(pk = transaction_id)
    eventmember = EventMember.objects.get(member=request.user, event=event)
    event.account.amount = float(event.account.amount) - float(transaction.amount)
    event.account.save()
    eventmember.account.amount = float(eventmember.account.amount) - float(transaction.amount)
    eventmember.account.save()
    messages.warning(request, 'The transaction is deleted !!!')
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))

def object_cost(request, event_id, cost_id):
    event = Event.objects.get(pk = event_id)
    eventmember = EventMember.objects.get(event=event, member=request.user)
    cost = Cost.objects.get(pk = cost_id)
    people_objected = cost.objected_by.all()
    if eventmember in people_objected:
        messages.success(request, 'You already objected the COST !!! ')
        return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))
    cost.is_objected = True
    cost.objected_by.add(eventmember)
    cost.save()
    messages.success(request, 'The cost is objected !!! ')
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))
