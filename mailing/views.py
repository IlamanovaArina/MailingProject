from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, TemplateView)
# from django.db.models import Count
from django.urls import reverse_lazy
from mailing.forms import MailForm, RecipientForm, MailingForm
from mailing.models import Recipient, Mail, Mailing, TryRecipient
# from django.shortcuts import render


# Классы представления для Mailing по принципу CRUD
class MailingListView(ListView):
    model = Mailing
    template_name = "home.html"
    context_object_name = 'mailings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Количество всех рассылок
        context['mailing_all'] = Mailing.objects.all().count()
        # Количество запущенных рассылок
        context['status_started'] = Mailing.objects.filter(my_field=Mailing.STATUS_STARTED).count()
        # Количество уникальных получателей
        context['recipient_all'] = Recipient.objects.all().count()
        return context


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем всех получателей этой рассылки
        context['recipients'] = self.object.recipient.all()
    #     context['mails'] = Mail.objects.all()
    #     context['mailings'] = Mailing.objects.select_related('mail', 'recipient').all()
        return context


class CombinedTemplateView(TemplateView):
    model = Mailing
    template_name = 'mailing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailings'] = Mailing.objects.all()
        context['mails'] = Mail.objects.all()
        context['recipients'] = Recipient.objects.all()
        return context


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailForm
    success_url = reverse_lazy('mailing:mailing')
    template_name = 'create.html'

    def form_valid(self, form):
        # Устанавливаем владельца на текущего авторизованного пользователя
        form.instance.owner = self.request.user
        # self.permissions_owner()
        return super().form_valid(form)

    def get_form_class(self):
        return MailingForm


class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = 'editing.html'
    success_url = reverse_lazy('mailing:mailing')

    def get_form_class(self):
        return MailingForm


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'delete.html'
    success_url = reverse_lazy('mailing:mailing')


# Классы представления для TryRecipient по принципу CRUD
class TryRecipientDeleteView(DeleteView):
    model = TryRecipient
    template_name = 'delete.html'


class TryRecipientListView(ListView):
    model = TryRecipient
    template_name = 'mailing_detail.html'


class TryRecipientUpdateView(UpdateView):
    model = TryRecipient
    template_name = 'editing.html'

    # def get_form_class(self):
    #     return MailingForm


class TryRecipientDetailView(DetailView):
    model = TryRecipient
    template_name = 'mailing_detail.html'


# class TryRecipientCreateView(CreateView):
#     model = TryRecipient
#     form_class =
#     success_url = reverse_lazy('mailing:mailing')
#     template_name = 'create.html'
#
#     def form_valid(self, form):
#         # Устанавливаем владельца на текущего авторизованного пользователя
#         form.instance.owner = self.request.user
#         # self.permissions_owner()
#         return super().form_valid(form)


# Классы представления для Recipient по принципу CRUD
class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy('mailing:mailing')
    template_name = 'create.html'

    def form_valid(self, form):
        # Устанавливаем владельца на текущего авторизованного пользователя
        form.instance.owner = self.request.user
        # self.permissions_owner()
        return super().form_valid(form)

    def get_form_class(self):
        return RecipientForm


class RecipientDetailView(DetailView):
    model = Recipient
    template_name = 'mailing.html'


class RecipientListView(ListView):
    model = Recipient
    template_name = 'mailing_detail.html'
    context_object_name = 'tryrecipients'


class RecipientUpdateView(UpdateView):
    model = Recipient
    template_name = 'editing.html'
    success_url = reverse_lazy('mailing:mailing')

    def get_form_class(self):
        return RecipientForm


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = 'delete.html'
    success_url = reverse_lazy('mailing:mailing')


# Классы представления для Mail по принципу CRUD
class MailCreateView(CreateView):
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('mailing:mailing')
    template_name = 'create.html'

    def form_valid(self, form):
        # Устанавливаем владельца на текущего авторизованного пользователя
        form.instance.owner = self.request.user
        # self.permissions_owner()
        return super().form_valid(form)

    def get_form_class(self):
        return MailForm


class MailDetailView(DetailView):
    model = Mail
    template_name = 'mailing_detail.html'


class MailListView(ListView):
    model = Mail


class MailUpdateView(UpdateView):
    model = Mail
    template_name = 'editing.html'
    success_url = reverse_lazy('mailing:mailing')

    def get_form_class(self):
        return MailForm


class MailDeleteView(DeleteView):
    model = Mail
    template_name = 'delete.html'
    success_url = reverse_lazy('mailing:mailing')

