import math
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import Event, EventMember, Cost
from user.models import MyUser, UserInfo
from account.models import Account, Transaction
from polls.models import Question
from jamah.models import JamahMember, Jamah
from polls.forms import QuestionCreateForm
from account.forms import TransactionForm
from .forms import EventCreateForm, CostCreateForm, UserAddForm


def do(request):
    # events = Event.objects.all()
    # for event in events:
    #     eventmembers = EventMember.objects.filter(event=event)
    #     for eventmember in eventmembers:
    #         if not eventmember.is_accountant:
    #             eventmember.accountant_account.delete()

    return HttpResponseRedirect(reverse('event:index'))

def index(request):
    template = loader.get_template('event/index.html')
    if request.user.is_authenticated:
        form = EventCreateForm()
        eventbyme = Event.objects.filter(creator = request.user)
        eventbyall = request.user.event_set.exclude(creator = request.user)
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
        left_jamah_members = JamahMember.objects.filter(
            jamah=event.jamah
        ).exclude(
            member__in = event.members.all()
        ).exclude(
            still_to_be_excepted = True
        )
        users_to_add = []
        for left in left_jamah_members:
            users_to_add.append(left.member)
        candidate_accountants = EventMember.objects.filter(event=event).exclude(is_accountant=True)
        candidate_observers = EventMember.objects.filter(event=event).exclude(is_cost_observer=True)
        # print(candidate_accountants)
        template = loader.get_template('event/detail.html')
        eventmembers = EventMember.objects.filter(event=event)
        polls = event.polls.all()
        costs = event.cost_set.all()
        pollform = QuestionCreateForm()
        costform = CostCreateForm()
        userform = UserAddForm()
        transaction_form = TransactionForm()
        accountants = EventMember.objects.filter(event=event, is_accountant=True)
        transaction_form.fields['accountant'].choices = [(accountant.id ,accountant.member.username) for accountant in accountants]
        choices = [(accountant.id ,accountant.member.username) for accountant in accountants]
        choices.append((0, 'Myself*'))
        costform.fields['from_accountant_or_myself'].choices = choices
        transactions = []
        for accountant in accountants:
            for transaction in accountant.accountant_account.transaction_ins.all():
                transactions.append(transaction)
        donations = event.account.transaction_ins.filter(is_donation = True)
        total_donation = 0
        for donation in donations:
            total_donation += donation.amount
        # todo use forms.py for this
        # userform.fields['choice'].choices = users_to_add
        context = {
            'total_donation': total_donation,
            'candidate_observers': candidate_observers,
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
    eventmembers = EventMember.objects.filter(event=event)# TODO: order by timestamp
    accountants = EventMember.objects.filter(event=event, is_accountant=True)
    observers = EventMember.objects.filter(event=event, is_cost_observer=True)
    polls = event.polls.all()
    costs = event.cost_set.all()
    transactions = []
    for accountant in accountants:
        for transaction in accountant.accountant_account.transaction_ins.all():
            transactions.append(transaction)
    donations = event.account.transaction_ins.filter(is_donation = True)
    context = {
        'observers': observers,
        'accountants': accountants,
        'costs': costs,
        'transactions': transactions,
        'current_eventmember': current_eventmember,
        'eventmembers': eventmembers,
        'polls': polls,
        'event': event,
    }
    template = loader.get_template('event/edit.html')
    return HttpResponse(template.render(context, request))

def finance(request, event_id):
    event = Event.objects.get(pk = event_id)
    current_eventmember = EventMember.objects.get(event=event, member=request.user)
    costs = event.cost_set.all()
    transactions = []
    accountants = EventMember.objects.filter(event=event, is_accountant=True)
    for accountant in accountants:
        for transaction in accountant.accountant_account.transaction_ins.all():
            transactions.append(transaction)
    total_donation = 0.00
    general_transactions = []
    donation_transactions = []
    event.account.amount = 0
    for transaction in transactions:
        if transaction.is_donation:
            donation_transactions.append(transaction)
            total_donation += float(transaction.amount)
            event.account.amount += transaction.amount
        else:
            general_transactions.append(transaction)
            event.account.amount = event.account.amount + transaction.amount
    event.account.save()
    event.total_donation = total_donation
    event.total_recieved_money = float(event.account.amount) - total_donation
    event.save()
    context = {
        'total_donation': total_donation,
        'donations': donation_transactions,
        'costs': costs,
        'transactions': general_transactions,
        'current_eventmember': current_eventmember,
        'event': event,
    }
    template = loader.get_template('event/event_finance.html')
    return HttpResponse(template.render(context, request))

def create_cost(request, event_id):
    event = Event.objects.get(pk = event_id)

    if request.method == 'POST':
        name = request.POST['name']
        amount = request.POST['amount']
        accountant_id = request.POST['from_accountant_or_myself']
        current_eventmember = EventMember.objects.get(event=event, member=request.user)
        # print(eventmember.member.username)
        # print(current_eventmember.member.username)
        print(accountant_id)
        if accountant_id == '0':
            transaction = Transaction(amount=amount,comes_from=request.user.info.account,goes_to=event.cost_account).save()
            print(transaction)
        else:
            accountant = EventMember.objects.get(pk = accountant_id)
            transaction = Transaction(amount=amount,comes_from=accountant.accountant_account,goes_to=event.cost_account).save()
            print(transaction)
        cost = Cost(amount=amount, name=name, added_by=current_eventmember, event=event)
        cost.save()
        event.total_cost = float(event.total_cost) + float(cost.amount)
        event.save()
        messages.success(request, 'Added COST to this Event !!! ')
        return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))
    else:
        costform = CostCreateForm()
        accountants = EventMember.objects.filter(event=event, is_accountant=True)
        choices = [(accountant.id ,accountant.member.username) for accountant in accountants]
        choices.append((0, 'Myself*'))
        costform.fields['from_accountant_or_myself'].choices = choices
        context = {
            'costform': costform,
            'event': event,
        }
        template = loader.get_template('event/create_cost.html')
        return HttpResponse(template.render(context, request))

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
            event.per_head_cost = (float(event.total_cost)/event.members.count())
            eventMember = EventMember(member=user, event=event).save()
            messages.success(request, 'The member is added in the event')
        else:
            messages.warning(request, 'The member is already in the event')
    event.save()
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))

def remove_member(request, event_id, member_id):
    event = Event.objects.get(pk = event_id)
    member = MyUser.objects.get(pk = member_id)
    eventmember = EventMember.objects.get(event=event, member=member)
    eventmember.accountant_account.delete()
    eventmember.delete()
    event.members.remove(member)
    event.save()
    # print(event.members.all())
    return HttpResponseRedirect(reverse('event:edit', args = (event_id,)))

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
    return HttpResponseRedirect(reverse('event:edit', args = (event_id,)))

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
    return HttpResponseRedirect(reverse('event:edit', args = (event_id,)))

def add_accountants(request, event_id):
    event = Event.objects.get(pk = event_id)
    values = request.POST.getlist('member')
    for value in values:
        user = MyUser.objects.get(pk = value)
        eventmember = EventMember.objects.get(member=user, event=event)
        eventmember.is_accountant = True
        account = Account(description = 'Event: ' + event.name + ' ' + ' ,Accountant: ' + user.username)
        account.mother_account = event.account
        account.save()
        eventmember.accountant_account = account
        eventmember.save()
    event.save()
    messages.success(request, 'Successfully added Accountant !!!')
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))

def add_observers(request, event_id):
    event = Event.objects.get(pk = event_id)
    values = request.POST.getlist('member')
    for value in values:
        user = MyUser.objects.get(pk = value)
        eventmember = EventMember.objects.get(member=user, event=event)
        eventmember.is_cost_observer = True
        eventmember.save()
    event.save()
    messages.success(request, 'Successfully added Observer !!!')
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))

def create_event_poll(request, event_id):
    event = Event.objects.get(pk = event_id)
    question_text = request.POST['question_text']
    poll = Question(question_text=question_text, creator=request.user, event=event).save()
    messages.success(request, 'Added a Poll for the event...')
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))

def make_transaction(request, event_id):
    event = Event.objects.get(pk = event_id)
    if request.method == 'POST':
        is_donation = request.POST.getlist('is_donation')
        amount = request.POST['amount']
        accountant_id = request.POST['accountant']
        accountant = EventMember.objects.get(pk = accountant_id)
        eventmember = EventMember.objects.get(member=request.user, event=event)
        user_account = request.user.info.account
        if len(is_donation):
            transaction = Transaction(amount=amount, goes_to=accountant.accountant_account, comes_from=user_account, is_donation=True)
        else:
            transaction = Transaction(amount=amount, goes_to=accountant.accountant_account, comes_from=user_account)
        transaction.save()
        messages.success(request, 'Added Money to the event with your name')
        return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))
    else:
        transaction_form = TransactionForm()
        accountants = EventMember.objects.filter(event=event, is_accountant=True)
        transaction_form.fields['accountant'].choices = [(accountant.id ,accountant.member.username) for accountant in accountants]
        context = {
            'event': event,
            'transaction_form': transaction_form
        }
        template = loader.get_template('event/transaction.html')
        return HttpResponse(template.render(context, request))

def verify_transaction(request, event_id, transaction_id):
    event = Event.objects.get(pk = event_id)
    transaction = Transaction.objects.get(pk = transaction_id)
    money_from_eventmember = EventMember.objects.get(member=transaction.comes_from.userinfo.user, event=event)
    accountant = EventMember.objects.get(member=request.user, event=event)
    if transaction.goes_to.eventmember == accountant:
        transaction.verified_by = request.user
        accountant.total_verified += transaction.amount
        accountant.save()
        transaction.save()
        if transaction.is_donation:
            money_from_eventmember.total_donation += transaction.amount
        else:
            money_from_eventmember.total_sent_money += transaction.amount
        money_from_eventmember.save()
        event.account.amount += transaction.amount
        event.account.save()
        accountant.accountant_account.amount += transaction.amount
        accountant.accountant_account.save()
        messages.success(request, 'The transaction is Verified !!!')
    else:
        messages.warning(request, 'You are not Authorized to verify !!!')
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))

def deny_transaction(request, event_id, transaction_id):
    messages.success(request, 'Replace the code!!!')
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))

def remove_verification(request, event_id, transaction_id):
    event = Event.objects.get(pk = event_id)
    transaction = Transaction.objects.get(pk = transaction_id)
    eventmember = EventMember.objects.get(member=request.user, event=event)
    if eventmember.is_accountant:
        if transaction.verified_by == request.user:
            transaction.verified_by = None
            eventmember.total_verified -= transaction.amount
            eventmember.save()
            transaction.save()
            messages.success(request, 'Transaction Verification is removed !!!')
        else:
            messages.warning(request, 'You can not remove Verification for this Transaction !!!')
    return HttpResponseRedirect(reverse('event:edit', args = (event_id,)))

def delete_transaction(request, event_id, transaction_id):
    event = Event.objects.get(pk = event_id)
    transaction = Transaction.objects.get(pk = transaction_id)
    eventmember = EventMember.objects.get(member=request.user, event=event)
    event.account.amount = float(event.account.amount) - float(transaction.amount)
    event.account.save()
    eventmember.accountant_account.amount = float(eventmember.accountant_account.amount) - float(transaction.amount)
    eventmember.accountant_account.save()
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
