from django.urls import path
from . import views

app_name = 'event'

urlpatterns = [
    path('', views.index, name = 'index'),
    # path('create', views.create, name = 'create'),
    path('<int:event_id>/create_event_poll', views.create_event_poll, name = 'create_event_poll'),
    path('<int:event_id>/create_cost', views.create_cost, name = 'create_cost'),
    path('<int:event_id>/<int:cost_id>/delete_cost', views.delete_cost, name = 'delete_cost'),
    path('<int:event_id>', views.detail, name = 'detail'),
    path('<int:event_id>/save_member', views.save_member, name = 'save_member'),
    path('<int:event_id>/<int:member_id>/remove_member', views.remove_member, name = 'remove_member'),
    path('<int:event_id>/pay', views.pay, name = 'pay'),
    path('<int:event_id>/donate', views.donate, name = 'donate'),
    path('<int:event_id>/make_transaction', views.make_transaction, name = 'make_transaction'),
    # TODO: add event financial state instead
    # path('<int:event_id>/cost/<int:cost_id>', views.cost_detail, name='cost_detail')
]
