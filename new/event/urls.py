from django.urls import path
from . import views

app_name = 'event'

urlpatterns = [
    path('', views.index, name = 'index'),
    # path('create', views.create, name = 'create'),
    path('<int:event_id>/create_event_poll', views.create_event_poll, name = 'create_event_poll'),
    path('<int:event_id>', views.detail, name = 'detail'),
    path('<int:event_id>/save_member', views.save_member, name = 'save_member'),
    path('<int:event_id>/<int:member_id>/remove_member', views.remove_member, name = 'remove_member'),
    path('<int:event_id>/pay', views.pay, name = 'pay'),
    path('<int:event_id>/donate', views.donate, name = 'donate'),
]
