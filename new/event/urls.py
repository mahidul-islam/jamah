from django.urls import path
from . import views

app_name = 'event'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:event_id>/create_event_poll', views.create_event_poll, name = 'create_event_poll'),
    path('<int:event_id>/create_cost', views.create_cost, name = 'create_cost'),
    path('<int:event_id>/cost/<int:cost_id>/delete', views.delete_cost, name = 'delete_cost'),
    path('<int:event_id>/cost/<int:cost_id>/object', views.object_cost, name = 'object_cost'),
    path('<int:event_id>', views.detail, name = 'detail'),
    path('<int:event_id>/finance', views.finance, name = 'finance'),
    path('<int:event_id>/edit', views.edit, name = 'edit'),
    path('<int:event_id>/save_member', views.save_member, name = 'save_member'),
    path('<int:event_id>/add_accountants', views.add_accountants, name = 'add_accountants'),
    path('<int:event_id>/<int:member_id>/remove_member', views.remove_member, name = 'remove_member'),
    path('<int:event_id>/<int:member_id>/promote_member', views.promote_member, name = 'promote_member'),
    path('<int:event_id>/<int:member_id>/demote_member', views.demote_member, name = 'demote_member'),
    path('<int:event_id>/transact', views.transact, name = 'transact'),
    path('<int:event_id>/transaction/<int:transaction_id>/verify', views.verify_transaction, name = 'verify_transaction'),
    path('<int:event_id>/transaction/<int:transaction_id>/remove_verification', views.remove_verification, name = 'remove_verification'),
    path('<int:event_id>/transaction/<int:transaction_id>/delete', views.delete_transaction, name = 'delete_transaction'),
    path('<int:event_id>/make_transaction', views.make_transaction, name = 'make_transaction'),
    # TODO: add event financial state instead
    # path('<int:event_id>/cost/<int:cost_id>', views.cost_detail, name='cost_detail')
]
