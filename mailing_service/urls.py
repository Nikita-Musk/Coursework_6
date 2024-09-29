from django.urls import path
from django.views.decorators.cache import cache_page
from mailing_service.apps import MailingServiceConfig
from mailing_service.views import MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, \
    MailingDeleteView, ClientListView, ClientCreateView, ClientUpdateView, ClientDetailView, ClientDeleteView, \
    MessageListView, MessageCreateView, MessageUpdateView, MessageDetailView, IndexListView

app_name = MailingServiceConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/create', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/update', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/<int:pk>/detail', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/<int:pk>/delete', MailingDeleteView.as_view(), name='mailing_delete'),

    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/create', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/update', ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/detail', ClientDetailView.as_view(), name='client_detail'),
    path('clients/<int:pk>/delete', ClientDeleteView.as_view(), name='client_delete'),

    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/create', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/update', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/detail', MessageDetailView.as_view(), name='message_detail'),
    path('message/<int:pk>/delete', MessageDetailView.as_view(), name='message_delete'),

    path('index/', cache_page(60)(IndexListView.as_view()), name='index'),

]
