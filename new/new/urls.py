from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('admin/', admin.site.urls),
    path('product/', include('product.urls')),
    path('polls/', include('polls.urls')),
    path('user/', include('user.urls')),
    path('profile/', include('userProfile.urls')),
    path('user/', include('django.contrib.auth.urls')),
    path('event/', include('event.urls')),
    # path('accountant/', include('accountant.urls'))
]
