from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('users.urls', namespace='users')),
    path('', include('mailing.urls', namespace='mailing')),
]
