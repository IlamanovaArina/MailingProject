from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import MailingDeleteView, MailingUpdateView, TryRecipientListView, \
    TryRecipientDeleteView, TryRecipientUpdateView, RecipientListView, \
    RecipientCreateView, RecipientUpdateView, RecipientDeleteView, MailListView, MailCreateView, \
    MailUpdateView, MailDeleteView, MailingListView, MailingDetailView, MailDetailView, RecipientDetailView, \
    TryRecipientDetailView

app_name = MailingConfig.name

urlpatterns = [
    path('home/', MailingListView.as_view(), name='home'),
    path('<int:pk>/detail/', MailingDetailView.as_view(), name='mailing_detail'),
    path('', MailingDeleteView.as_view(), name=''),
    path('', MailingUpdateView.as_view(), name=''),

    path('', TryRecipientListView.as_view(), name=''),
    path('', TryRecipientDeleteView.as_view(), name=''),
    path('', TryRecipientDetailView.as_view(), name=''),
    path('', TryRecipientUpdateView.as_view(), name=''),


    path('', RecipientListView.as_view(), name=''),
    path('', RecipientDetailView.as_view(), name=''),
    path('', RecipientCreateView.as_view(), name=''),
    path('', RecipientDeleteView.as_view(), name=''),
    path('', RecipientUpdateView.as_view(), name=''),

    path('', MailListView.as_view(), name=''),
    path('<int:pk>/detail/', MailDetailView.as_view(), name='mailing_detail'),
    path('', MailCreateView.as_view(), name=''),
    path('', MailUpdateView.as_view(), name=''),
    path('', MailDeleteView.as_view(), name=''),


]
