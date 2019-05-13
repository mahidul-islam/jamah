from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.allblog, name = 'allblog'),
    path('create', views.create, name = 'create'),
    path('<int:blog_id>', views.detail, name = 'detail')
]
