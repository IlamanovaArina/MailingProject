from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, TemplateView)
from mailing.models import Recipient, Mail, Mailing, TryRecipient
from django.shortcuts import render


# Классы представления для Mailing по принципу CRUD
class MailingListView(ListView):
    model = Mailing
    template_name = "home.html"
    context_object_name = 'mailings'


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipients'] = Recipient.objects.all()
        context['mails'] = Mail.objects.all()
        context['mailings'] = Mailing.objects.select_related('mail', 'recipient').all()
        return context


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = ''


class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = ''


# Классы представления для Recipient по принципу CRUD
class TryRecipientListView(ListView):
    model = TryRecipient
    template_name = ''


class TryRecipientDeleteView(DeleteView):
    model = TryRecipient
    template_name = ''


class TryRecipientDetailView(DetailView):
    model = TryRecipient
    template_name = 'mailing_detail.html'


class TryRecipientUpdateView(UpdateView):
    model = TryRecipient
    template_name = ''


# Классы представления для Recipient по принципу CRUD
class RecipientListView(ListView):
    model = Recipient
    template_name = ''


class RecipientDetailView(DetailView):
    model = Recipient
    template_name = ''


class RecipientCreateView(CreateView):
    model = Recipient


class RecipientDeleteView(DeleteView):
    model = Recipient


class RecipientUpdateView(UpdateView):
    model = Recipient
''


# Классы представления для Mail по принципу CRUD
class MailListView(ListView):
    model = Mail


class MailDetailView(DetailView):
    model = Mail
    template_name = 'mailing_detail.html'


class MailCreateView(CreateView):
    model = Mail


class MailUpdateView(UpdateView):
    model = Mail


class MailDeleteView(DeleteView):
    model = Mail


# class CombinedView(TemplateView):
#     template_name = 'mailing_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['mailings'] = Mailing.objects.all()
#         context['recipients'] = Recipient.objects.all()
#         context['tryrecipient'] = TryRecipient.objects.all()
#         context['mail'] = Mail.objects.all()
#         # context['mails'] = Mail.objects.select_related('mailing', 'recipient').all()
#         return context

