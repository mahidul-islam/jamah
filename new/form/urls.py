from django.urls import path

from . import views

urlpatterns = [
    path('', views.allProduct),
    path('<int:lowrange>/<int:highrange>', views.productInRange),
]
