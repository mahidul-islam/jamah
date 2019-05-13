from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('alluser', views.alluser, name='alluser'),
    path('<int:user_id>', views.profile, name='user_profile'),
    path('<int:user_id>', views.send_mail, name='send_mail')
]
