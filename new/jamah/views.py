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
    if request.user:
        form = JamahCreateForm()
        jamah_by_me = Jamah.objects.filter(creator = request.user)
        jamah_by_all = request.user.jamah_set.all()
        all_jamah = Jamah.objects.all()
        print(jamah_by_all)
        print('-----------------------------------------------------------------')
        context = {
            'form': form,
            'jamah_by_me': jamah_by_me,
            'jamah_by_all': jamah_by_all,
        }
        return HttpResponse(template.render(context, request))

    else:
        context = {}
        messages.success(request, 'Please Log in to use this feature')
        return HttpResponse(template.render(context, request))

def detail(request, jamah_id):
    return HttpResponse("This is jamah detail")

def create(request):
    print(request.POST)
    name = request.POST['jamahname']
    jamah = Jamah(jamahname = name, creator = request.user)
    jamah.save()
    jamah.members.add(request.user)
    jamah.save()
    jamahMember = JamahMember(member=request.user, jamah=jamah, status='creator').save()
    print(jamahMember)
    return HttpResponseRedirect(reverse('jamah:index'))
