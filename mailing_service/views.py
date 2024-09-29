import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Blog
from mailing_service.forms import MailingForm, ClientForm, MessageForm, ManagerMailingForm
from mailing_service.models import Client, Mailing, Message


class MailingListView(LoginRequiredMixin,ListView):
    model = Mailing

class MailingDetailView(LoginRequiredMixin,DetailView):
    model = Mailing

class MailingCreateView(LoginRequiredMixin,CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing_service:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.owner = self.request.user
        mailing.save()
        mailing.clients.set(form.cleaned_data['clients'])
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin,UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing_service:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.get_form_class() == ManagerMailingForm:
            return kwargs
        else:
            kwargs['request'] = self.request
            return kwargs

    def form_valid(self, form):
        if isinstance(form, ManagerMailingForm):
            return super().form_valid(form)
        else:
            mailing = form.save(commit=False)
            mailing.clients.set(form.cleaned_data['clients'])
            return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return MailingForm
        elif user.has_perm('mailing_service.deactivate_mailing'):
            return ManagerMailingForm
        else:
            raise PermissionDenied


class MailingDeleteView(LoginRequiredMixin,DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing_service:mailing_list')

class ClientListView(LoginRequiredMixin,ListView):
    model = Client

class ClientDetailView(LoginRequiredMixin,DetailView):
    model = Client

class ClientCreateView(LoginRequiredMixin,CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing_service:client_list')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)

class ClientUpdateView(LoginRequiredMixin,UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing_service:client_list')

class ClientDeleteView(LoginRequiredMixin,DeleteView):
    model = Client
    success_url = reverse_lazy('mailing_service:client_list')

class MessageListView(LoginRequiredMixin,ListView):
    model = Message

class MessageDetailView(LoginRequiredMixin,DetailView):
    model = Message

class MessageCreateView(LoginRequiredMixin,CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing_service:message_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)

class MessageUpdateView(LoginRequiredMixin,UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing_service:message_list')

class MessageDeleteView(LoginRequiredMixin,DeleteView):
    model = Message
    success_url = reverse_lazy('mailing_service:message_list')

class IndexListView(ListView):
    model = Blog
    template_name = 'mailing_service/index.html'
    context_object_name = 'random_blogs'

    def get_queryset(self):
        posts = Blog.objects.all()
        random_post = random.sample(list(posts), 3)
        return random_post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailing'] = Mailing.objects.count()
        context['active_mailing'] = Mailing.objects.filter(status='started').count()
        context['unique_clients'] = Mailing.objects.values('clients').distinct().count()
        return context

