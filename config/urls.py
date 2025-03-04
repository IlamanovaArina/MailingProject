from django.contrib import admin
from django.conf.urls.static import static
from config import settings
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls', namespace='users')),
    path('mailing/', include('mailing.urls', namespace='mailing')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
