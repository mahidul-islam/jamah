from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('admin/', admin.site.urls),
    path('product/', include('form.urls')),
    path('polls/', include('polls.urls')),
    path('user/', include('user.urls')),
    path('user/', include('django.contrib.auth.urls')),
    # path('accountant/', include('accountant.urls'))
]
