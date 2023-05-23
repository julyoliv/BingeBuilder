from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from type_event.settings import MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('events/', include('events.urls')),
    path('client/', include('client.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
