from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from .models import Question, Choice, Comment


def index(request):
    question_list = Question.objects.all()
    template = loader.get_template('polls/index.html')
    context = {'question_list':question_list}
    return HttpResponse(template.render(context, request))

def latest(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/latest.html')
    context = {'latest_question_list' : latest_question_list}
    context2 = {}
    return HttpResponse(template.render(context, request))

def result(request, question_id):
    question = Question.objects.get(pk = question_id)
    template = loader.get_template('polls/result.html')
    context = {'question': question}
    return HttpResponse(template.render(context, request))
    # return HttpResponse(('you are looking at result of question no {}').format(question_id))

def vote(request, question_id):
    question = Question.objects.get(pk = question_id)
    try:
        choice = question.choice_set.get(pk = request.POST['choice'])
    except:
        context = {
            'error_message':'ERROR: you didnot select a choice',
            'question':question
        }
        template = loader.get_template('polls/detail.html')
        return HttpResponse(template.render(context, request))
    else:
        choice.votes += 1
        choice.save()
        return HttpResponseRedirect(reverse('polls:result', args = (question.id,)))


def detail(request, question_id):
    try:
        question = Question.objects.get(pk = question_id)
        context = {'question': question}
        templa = loader.get_template('polls/detail.html')
    except Question.DoesNotExist:
        raise Http404('question does not exist')
    return HttpResponse(templa.render(context, request))

def save_comment(request, question_id):
    question = Question.objects.get(pk = question_id)
    comment_text = request.POST['comment']
    Comment(comment_text = comment_text, pub_date = timezone.now(), question = question).save()
    return HttpResponseRedirect(reverse('polls:detail', args = (question_id,)))

def save_question(request):
    question_text = request.POST['question']
    Question(question_text = question_text, pub_date = timezone.now()).save()
    return HttpResponseRedirect(reverse('polls:index'))

def save_choice(request, question_id):
    question = Question.objects.get(pk = question_id)
    Choice(choice_text = request.POST['choice'], question = question, votes = 0).save()
    return HttpResponseRedirect(reverse('polls:detail', args = (question_id,)))
