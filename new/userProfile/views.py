from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from user.models import MyUser
from django.template import loader
from polls.models import Question
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def profile(request, user_id):
    user = MyUser.objects.get(pk = user_id)
    jamahs = user.jamahs_of_you.all()
    polls = user.question_set.exclude(is_part_of_event=True)
    context = {
        'polls': polls,
        'jamahs': jamahs,
        'user': user
    }
    template = loader.get_template('userProfile/profile.html')
    return HttpResponse(template.render(context, request))


def alluser(request):
    users = MyUser.objects.all()
    return HttpResponse('This is all user')

def send_mail(request, user_id):
    return HttpResponseRedirect(reverse('profile:user_profile', args = (user_id,)))
