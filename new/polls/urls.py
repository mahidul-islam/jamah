from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),
    path('latest', views.latest, name='latest'),
    path('<int:question_id>', views.detail, name='detail'),
    path('<int:question_id>/result', views.result, name='result'),
    path('<int:question_id>/vote', views.vote, name='vote'),
    # path('<int:question_id>/vote2', views.vote2, name='vote2'),
    path('<int:question_id>/comment/save', views.save_comment, name='save_comment'),
    path('<int:question_id>/choice/save', views.save_choice, name='save_choice'),
    path('question/save', views.save_question, name='save_question'),
    path('<int:question_id>/change_vote', views.change_vote, name='change_vote'),
    path('<int:question_id>/delete_question', views.delete_question, name='delete_question'),
]
