from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import *

app_name = MailingConfig.name

urlpatterns = [
    path('home/', MailingListView.as_view(), name='home'),
    # path('home/', ResultView.as_view(), name='home'),
    path('<int:pk>/detail/', MailingDetailView.as_view(), name='mailing_detail'),
    path('<int:pk>/send/', SendMessageDetailView.as_view(), name='home_send_message'),
    path('create/', CombinedTemplateView.as_view(), name='mailing'),
    path('create/mailing/', MailingCreateView.as_view(), name='create'),
    path('<int:pk>/edit_mailing/', MailingUpdateView.as_view(), name='edit_mailing'),
    path('<int:pk>/delete_mailing/', MailingDeleteView.as_view(), name='delete_mailing'),

    path('', TryRecipientDetailView.as_view(), name=''),
    path('<int:pk>/detail/', TryRecipientListView.as_view(), name='mailing_detail'),
    path('<int:pk>/edit_tryrecipients/', TryRecipientUpdateView.as_view(), name='edit_tryrecipients'),
    path('<int:pk>/delete_tryrecipients/', TryRecipientDeleteView.as_view(), name='delete_tryrecipients'),

    path('create/recipient/', RecipientCreateView.as_view(), name='create'),
    path('', RecipientDetailView.as_view(), name=''),
    path('<int:pk>/detail/', RecipientListView.as_view(), name='mailing_detail'),
    path('<int:pk>/edit_recipient/', RecipientUpdateView.as_view(), name='edit_recipient'),
    path('<int:pk>/delete_recipient/', RecipientDeleteView.as_view(), name='delete_recipient'),

    path('create/mail/', MailCreateView.as_view(), name='create'),
    path('<int:pk>/detail/', MailDetailView.as_view(), name='mailing_detail'),
    path('', MailListView.as_view(), name=''),
    path('<int:pk>/edit_mail/', MailUpdateView.as_view(), name='edit_mail'),
    path('<int:pk>/delete_mail/', MailDeleteView.as_view(), name='delete_mail'),


]
