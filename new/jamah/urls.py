from django.urls import path
from . import views

app_name = 'jamah'

urlpatterns = [
    path('', views.alljamah, name='all_jamah'),
    path('index', views.index, name='index'),
    path('<int:jamah_id>/join', views.join_jamah, name='join_jamah'),
    path('<int:jamah_id>', views.detail, name='detail'),
    path('create', views.create, name='create'),
]
