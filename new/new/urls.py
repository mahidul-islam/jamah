from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
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
    path('jamah/', include('jamah.urls')),    
    path('blog/', include('blog.urls'))
]   + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# TODO: add media file + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
