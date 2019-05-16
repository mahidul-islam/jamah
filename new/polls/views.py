from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from .models import Question, Choice, Comment, Vote
from django.contrib import messages


def index(request):
    # TODO: exclude all question associated with events...
    polls = Question.objects.all()
    template = loader.get_template('polls/index.html')
    context = {'polls':polls}
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
        # see if the user already voted for the question
        vote = question.vote_set.get(voter = request.user)
        # print(vote)
    except:
        # now we know that the user didnot vote
        try:
            # check if voter selected a choice
            choice = question.choice_set.get(pk = request.POST['choice'])
        except:
            # voter didnot selected a choice
            context = {
                'question':question
            }
            messages.warning(request, 'You didnot select a CHOICE')
            template = loader.get_template('polls/detail.html')
            return HttpResponse(template.render(context, request))
        else:
            # voter did select
            choice.votes += 1
            choice.save()
            Vote(question = question, voter = request.user, choice_no = choice.id).save()
            return HttpResponseRedirect(reverse('polls:result', args = (question.id,)))
    else:
        # the voter already voted
        context = {
            'question':question,
            'change':'change'
        }
        messages.warning(request, 'You already Voted!!!')
        template = loader.get_template('polls/detail.html')
        return HttpResponse(template.render(context, request))


def detail(request, question_id):
    try:
        question = Question.objects.get(pk = question_id)
        context = {'question': question}
        template = loader.get_template('polls/detail.html')
    except Question.DoesNotExist:
        raise Http404('question does not exist')
    return HttpResponse(template.render(context, request))

def save_comment(request, question_id):
    question = Question.objects.get(pk = question_id)
    comment_text = request.POST['comment']
    Comment(comment_text=comment_text, pub_date=timezone.now(), question=question, commenter=request.user).save()
    return HttpResponseRedirect(reverse('polls:detail', args = (question_id,)))

def save_question(request):
    question_text = request.POST['question']
    Question(question_text = question_text, pub_date = timezone.now(), creator = request.user).save()
    return HttpResponseRedirect(reverse('polls:index'))

def save_choice(request, question_id):
    question = Question.objects.get(pk = question_id)
    Choice(choice_text = request.POST['choice'], question = question, votes = 0, creator=request.user).save()
    return HttpResponseRedirect(reverse('polls:detail', args = (question_id,)))

def change_vote(request, question_id):
    question = Question.objects.get(pk = question_id)
    vote = question.vote_set.get(voter = request.user)
    choice_no = vote.choice_no
    choice = question.choice_set.get(pk = choice_no)
    choice.votes -= 1
    template = loader.get_template('polls/detail.html')
    context ={
        'question':question
    }
    vote.delete()
    choice.save()
    messages.info(request, 'Please VOTE again...')
    return HttpResponse(template.render(context, request))

def delete_question(request, question_id):
    question = Question.objects.get(pk = question_id)
    question.delete()
    template = loader.get_template('polls/index.html')
    context = {}
    return HttpResponseRedirect(reverse('polls:index'))
