from django.urls import path
from . import views

app_name = 'jamah'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:jamah_id>', views.detail, name='detail'),
    path('create', views.create, name='create'),
]
