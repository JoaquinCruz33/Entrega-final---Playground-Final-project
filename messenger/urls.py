from django.urls import path
from . import views

urlpatterns = [
    path('received/', views.ReceivedMessagesListView.as_view(), name='received_messages'),
    path('sent/', views.SentMessagesListView.as_view(), name='sent_messages'),
    path('new/', views.MessageCreateView.as_view(), name='send_message'),
    path('<int:pk>/', views.MessageDetailView.as_view(), name='message_detail'),
]