from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.allProduct, name='index'),
    path('<int:lowrange>/<int:highrange>', views.productInRange, name='productInRange'),
]
