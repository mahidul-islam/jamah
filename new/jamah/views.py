from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from .forms import JamahCreateForm
from event.forms import EventCreateForm
from .models import Jamah, JamahMember
from user.models import MyUser
from event.models import Event, EventMember
from account.models import Account


def index(request):
    template = loader.get_template('jamah/index.html')
    if request.user.is_authenticated:
        form = JamahCreateForm()
        jamah_by_me = Jamah.objects.filter(creator = request.user)
        jamah_by_all = request.user.jamahs_of_you.all()
        all_jamah = Jamah.objects.all()
        # print(jamah_by_all)
        # print('-----------------------------------------------------------------')
        context = {
            'form': form,
            'jamah_by_me': jamah_by_me,
            'jamah_by_all': jamah_by_all,
        }
        return HttpResponse(template.render(context, request))

    else:
        context = {}
        messages.info(request, 'Please Log in to use this feature')
        return HttpResponse(template.render(context, request))

def detail(request, jamah_id):
    jamah = Jamah.objects.get(pk = jamah_id)
    jamahmembers = jamah.members.all()
    events = jamah.events.all()
    template = loader.get_template('jamah/detail.html')
    form = EventCreateForm()
    context = {
        'eventForm': form,
        'events': events,
        'jamah': jamah,
    }
    return HttpResponse(template.render(context, request))

def alljamah(request):
    template = loader.get_template('jamah/jamahs.html')
    if request.user.is_authenticated:
        form = JamahCreateForm()
        all_jamah = Jamah.objects.all()
        context = {
            'form': form,
            'all_jamah': all_jamah,
        }
        return HttpResponse(template.render(context, request))
    else:
        context = {}
        messages.info(request, 'Please Log in to use this feature')
        return HttpResponse(template.render(context, request))

def join_jamah(request, jamah_id):
    jamah = Jamah.objects.get(pk = jamah_id)
    # test if he requested already
    jamahMember = JamahMember.objects.filter(member = request.user).filter(jamah = jamah)
    if jamahMember.count():
        jamahMember = jamahMember[0]
        if jamahMember.still_to_be_excepted:
            messages.success(request, 'You already requested to join !!!')
            return HttpResponseRedirect(reverse('jamah:all_jamah'))
        else:
            messages.success(request, 'You already are a Member !!!')
            return HttpResponseRedirect(reverse('jamah:all_jamah'))
    else:
        # user didnot requested before so create jamahMember
        jamah.requested_to_join.add(request.user)
        jamah.save()
        account = Account(description = 'Jamah: ' + jamah.jamahname + ' ' + ' ,Member: ' + request.user.username)
        account.save()
        jamahMember = JamahMember(member=request.user, jamah=jamah, status='member', account=account).save()
        messages.success(request, 'You requested to join the Group')
        return HttpResponseRedirect(reverse('jamah:all_jamah'))

def create(request):
    name = request.POST['jamahname']
    account = Account(description = 'Jamah: ' + name + '\'s account')
    account.save()
    jamah = Jamah(jamahname = name, creator = request.user, account=account)
    jamah.save()
    jamah.members.add(request.user)
    jamah.save()
    account2 = Account(description = 'Jamah: ' + name + ' ' + ' ,Member: ' + request.user.username)
    account2.save()
    jamahMember = JamahMember(
        member = request.user,
        jamah = jamah,
        status = 'creator',
        still_to_be_excepted = False,
        account = account2
    ).save()
    # print(jamahMember)
    return HttpResponseRedirect(reverse('jamah:all_jamah'))

def save_member(request, jamah_id, jamahmember_id):
    jamah = Jamah.objects.get(pk = jamah_id)
    jamahmember = JamahMember.objects.get(pk = jamahmember_id)
    jamahmember.still_to_be_excepted = False
    jamah.members.add(jamahmember.member)
    jamah.requested_to_join.remove(jamahmember.member)
    jamahmember.timestamp = timezone.now()
    jamah.save()
    jamahmember.save()
    return HttpResponseRedirect(reverse('jamah:detail', args = (jamah_id,)))

def remove_member(request, jamah_id, member_id):
    jamah = Jamah.objects.get(pk = jamah_id)
    member = MyUser.objects.get(pk = member_id)
    jamahmember = JamahMember.objects.get(jamah=jamah, member=member)
    jamahmember.account.delete()
    jamahmember.delete()
    jamah.members.remove(member)
    # print(event.members.all())
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))

def promote_member(request, jamah_id, member_id):
    jamah = Jamah.objects.get(pk = jamah_id)
    member = MyUser.objects.get(pk = member_id)
    jamahmember = JamahMember.objects.get(jamah=jamah, member=member)
    if jamahmember.status == 'member':
        jamahmember.status = 'admin'
    elif jamahmember.status == 'admin':
        jamahmember.status = 'modarator'
    jamahmember.save()
    # print(event.members.all())
    return HttpResponseRedirect(reverse('event:detail', args = (event_id,)))


def create_jamah_event(request, jamah_id):
    jamah = Jamah.objects.get(pk = jamah_id)
    name = request.POST['name']
    messages.success(request, 'Added a Event for the jamah...')
    account = Account(description = 'Event: ' + name + '\'s account')
    account.save()
    cost_account = Account(description = 'Event: ' + name + '\'s cost account')
    cost_account.save()
    event = Event(name = name, creator = request.user, account = account, jamah=jamah, cost_account=cost_account)
    event.save()
    event.members.add(request.user)
    event.save()
    member_account = Account(description = 'Event: ' + name + ' ' + ' ,Member: ' + request.user.username)
    member_account.mother_account = event.account
    member_account.save()
    eventMember = EventMember(
        member = request.user,
        event = event,
        status = 'creator',
        accountant_account = member_account,
        is_accountant = True,
        is_head_accountant = True,
        is_cost_observer = True,
        ).save()
    return HttpResponseRedirect(reverse('jamah:detail', args = (jamah_id,)))
