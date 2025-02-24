from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import HomeListView

# from mailing.views import (RecipientListView, RecipientDetailView, RecipientCreateView, RecipientUpdateView,
#                             RecipientDeleteView, MailListView, MailDetailView, MailCreateView, MailUpdateView,
#                             MailDeleteView, HomeListView)


app_name = MailingConfig.name

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),

    # path('recipient/', RecipientListView.as_view(), name='recipient'),
    # path('recipient/<int:pk>/', RecipientDetailView.as_view(), name='recipient_detail'),
    # path('recipient/create/', RecipientCreateView.as_view(), name='recipient_create'),
    # path('recipient/<int:pk>/update/', RecipientUpdateView.as_view(), name='recipient_update'),
    # path('recipient/<int:pk>/delete/', RecipientDeleteView.as_view(), name='recipient_delete'),
    #
    # path('mail/', MailListView.as_view(), name='mail'),
    # path('mail/<int:pk>/', MailDetailView.as_view(), name='mail_detail'),
    # path('mail/create/', MailCreateView.as_view(), name='mail_create'),
    # path('mail/<int:pk>/update/', MailUpdateView.as_view(), name='mail_update'),
    # path('mail/<int:pk>/delete', MailDeleteView.as_view(), name='mail_delete'),
]