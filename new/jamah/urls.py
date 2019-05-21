from django.urls import path
from . import views

app_name = 'jamah'

urlpatterns = [
    path('', views.alljamah, name='all_jamah'),
    path('index', views.index, name='index'),
    path('<int:jamah_id>/join', views.join_jamah, name='join_jamah'),
    path('<int:jamah_id>', views.detail, name='detail'),
    path('create', views.create, name='create'),
    path('<int:jamah_id>/<int:jamahmember_id>', views.save_member, name='save_member'),
    path('<int:jamah_id>/create_jamah_event', views.create_jamah_event, name = 'create_jamah_event'),
]
