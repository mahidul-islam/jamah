from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from .models import Question, Choice, Comment, Vote
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from rules.contrib.views import permission_required
from .forms import QuestionCreateForm, ChoiceCreateForm, CommentCreateForm, VoteCreateForm
import rules


@rules.predicate
def is_poll_creator(user, poll):
    return poll.creator == user

def vote_count(question_id):
    question = Question.objects.get(pk = question_id)
    votes = question.vote_set.all()
    choices = question.choice_set.all()
    for choice in choices:
        print(choice)
        choice.votes = 0
        choice.save()
    for vote in votes:
        print(vote)
        vote.choice.votes += 1
        vote.choice.save()
    for choice in choices:
        print(choice.votes)

def index(request):
    # TODO: exclude all question associated with events...
    polls = Question.objects.all()
    template = loader.get_template('polls/index.html')
    data = {'creator':request.user}
    form = QuestionCreateForm(initial=data)
    context = {
        'polls':polls,
        'form':form,
    }
    return HttpResponse(template.render(context, request))

def latest(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    data = {'creator':request.user}
    form = QuestionCreateForm(initial=data)
    context = {
        'polls':polls,
        'form':form,
    }
    return HttpResponse(template.render(context, request))


def result(request, question_id):
    question = Question.objects.get(pk = question_id)
    template = loader.get_template('polls/result.html')
    choices = question.choice_set.all().order_by('pub_date')
    context = {
        'question': question,
        'choices': choices,
    }
    return HttpResponse(template.render(context, request))
    # return HttpResponse(('you are looking at result of question no {}').format(question_id))

def vote(request, question_id):
    question = Question.objects.get(pk = question_id)
    choiceForm = ChoiceCreateForm()
    commentForm = CommentCreateForm()

    if request.user:
        try:
            # see if the user already voted for the question
            vote = question.vote_set.get(voter = request.user)
            # print(vote)
        except Vote.DoesNotExist:
            # now we know that the user didnot vote
            try:
                # check if voter selected a choice
                choice = question.choice_set.get(pk = request.POST['choice'])
                # print('......................................................')
                # print(request.POST)
                # print(choice)
                # print('---------------------------------------------------------')
            except :
                # voter didnot selected a choice
                context = {
                    'question':question,
                    'choiceForm': choiceForm,
                    'commentForm': commentForm,
                }
                messages.warning(request, 'You didnot select a CHOICE')
                template = loader.get_template('polls/detail.html')
                return HttpResponse(template.render(context, request))
            else:
                Vote(question = question, voter = request.user, choice_no = choice.id, choice = choice).save()
                vote_count(question_id)
                return HttpResponseRedirect(reverse('polls:result', args = (question.id,)))
        else:
            # the voter already voted
            context = {
                'question': question,
                'choiceForm': choiceForm,
                'commentForm': commentForm,
                'change': True,
            }
            messages.warning(request, 'You already Voted!!!')
            template = loader.get_template('polls/detail.html')
            return HttpResponse(template.render(context, request))
    else:
        context = {
            'question': question,
            'choiceForm': choiceForm,
            'commentForm': commentForm,
        }
        messages.warning(request, 'You NEED to logIN to VOTE!!!')
        template = loader.get_template('polls/detail.html')
        return HttpResponse(template.render(context, request))


def detail(request, question_id):
    try:
        question = Question.objects.get(pk = question_id)
        choiceForm = ChoiceCreateForm()
        commentForm = CommentCreateForm()
        voteForm = VoteCreateForm()
        context = {
            'question': question,
            'choiceForm': choiceForm,
            'commentForm': commentForm,
            'voteForm': voteForm,
        }
        template = loader.get_template('polls/detail.html')
    except Question.DoesNotExist:
        raise Http404('question does not exist')
    return HttpResponse(template.render(context, request))

def save_comment(request, question_id):
    question = Question.objects.get(pk = question_id)
    comment_text = request.POST['comment_text']
    Comment(comment_text=comment_text, pub_date=timezone.now(), question=question, commenter=request.user).save()
    return HttpResponseRedirect(reverse('polls:detail', args = (question_id,)))

def save_question(request):
    if request.user.is_authenticated:
        print(request.POST)
        question_text = request.POST['question_text']
        poll = Question(question_text=question_text, creator=request.user).save()
        messages.success(request, 'Added Another Poll...')
        return HttpResponseRedirect(reverse('polls:index'))
    else:
        messages.warning(request, 'Log in to add Poll!!!')
        return HttpResponseRedirect(reverse('polls:index'))

def save_choice(request, question_id):
    question = Question.objects.get(pk = question_id)
    Choice(choice_text = request.POST['choice_text'], question = question, votes = 0, creator=request.user).save()
    return HttpResponseRedirect(reverse('polls:detail', args = (question_id,)))

def change_vote(request, question_id):
    question = Question.objects.get(pk = question_id)
    vote = question.vote_set.get(voter = request.user)
    template = loader.get_template('polls/detail.html')
    choiceForm = ChoiceCreateForm()
    commentForm = CommentCreateForm()
    context = {
        'question': question,
        'choiceForm': choiceForm,
        'commentForm': commentForm,
    }
    vote.delete()
    messages.info(request, 'Please VOTE again...')
    return HttpResponse(template.render(context, request))

rules.add_perm('polls.can_delete_poll', is_poll_creator)

def delete_question(request, question_id):
    question = Question.objects.get(pk = question_id)
    if request.user.has_perm('polls.can_delete_poll', question):
        question.delete()
        template = loader.get_template('polls/index.html')
        context = {}
        return HttpResponseRedirect(reverse('polls:index'))
    else:
        messages.warning(request, 'You do not have required permission')
        return HttpResponseRedirect(reverse('polls:index'))
