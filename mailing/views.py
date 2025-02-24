from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from mailing.models import Recipient, Mail, Mailing


class HomeListView(ListView):
    model = Mailing
    template_name = "home.html"


# class RecipientListView(ListView):
#     model = Recipient
#
#
# class RecipientDetailView(DetailView):
#     model = Recipient
#
#
# class RecipientCreateView(CreateView):
#     model = Recipient
#
#
# class RecipientDeleteView(DeleteView):
#     model = Recipient
#
#
# class RecipientUpdateView(UpdateView):
#     model = Recipient
#
#
# class MailListView(ListView):
#     model = Mail
#
#
# class MailDetailView(DetailView):
#     model = Mail
#
#
# class MailCreateView(CreateView):
#     model = Mail
#
#
# class MailUpdateView(UpdateView):
#     model = Mail
#
#
# class MailDeleteView(DeleteView):
#     model = Mail
#
#
# class MailingListView(ListView):
#     model = Mailing
#
#
# class MailingDetailView(DetailView):
#     model = Mailing
#
#
# class MailingListView(ListView):
#     model = Mailing
#
#
# class MailingListView(ListView):
#     model = Mailing
#
#
# class MailingListView(ListView):
#     model = Mailing

