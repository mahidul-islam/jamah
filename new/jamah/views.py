from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import Jamah, JamahMember
from django.urls import reverse
from user.models import MyUser
from django.contrib import messages
from .forms import JamahCreateForm


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
    return HttpResponse("This is jamah detail")

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
        jamahMember = JamahMember(member=request.user, jamah=jamah, status='member').save()
        messages.success(request, 'You requested to join the Group')
        return HttpResponseRedirect(reverse('jamah:all_jamah'))

def create(request):
    print(request.POST)
    name = request.POST['jamahname']
    jamah = Jamah(jamahname = name, creator = request.user)
    jamah.save()
    jamah.members.add(request.user)
    jamah.save()
    jamahMember = JamahMember(member=request.user, jamah=jamah, status='creator', still_to_be_excepted=False).save()
    # print(jamahMember)
    return HttpResponseRedirect(reverse('jamah:all_jamah'))
