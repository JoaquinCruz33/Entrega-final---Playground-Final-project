from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q # Para búsquedas OR

from .models import Message
from .forms import MessageForm
from django.contrib.auth.models import User # Para seleccionar destinatarios

# Vista para listar mensajes recibidos
class ReceivedMessagesListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messenger/received_messages.html'
    context_object_name = 'messages'
    paginate_by = 10

    def get_queryset(self):
        # Obtiene solo los mensajes donde el usuario actual es el receptor
        return Message.objects.filter(receiver=self.request.user).order_by('-sent_at')

# Vista para listar mensajes enviados
class SentMessagesListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messenger/sent_messages.html'
    context_object_name = 'messages'
    paginate_by = 10

    def get_queryset(self):
        # Obtiene solo los mensajes donde el usuario actual es el remitente
        return Message.objects.filter(sender=self.request.user).order_by('-sent_at')

# Vista para ver el detalle de un mensaje
class MessageDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Message
    template_name = 'messenger/message_detail.html'
    context_object_name = 'message'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Marcar el mensaje como leído si el usuario actual es el receptor
        if obj.receiver == self.request.user and not obj.is_read:
            obj.is_read = True
            obj.save()
        return obj

    def test_func(self):
        # Solo el remitente o el receptor pueden ver el mensaje
        message = self.get_object()
        return self.request.user == message.sender or self.request.user == message.receiver

# Vista para enviar un nuevo mensaje
class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'messenger/message_form.html'
    success_url = reverse_lazy('sent_messages') # Redirige a los mensajes enviados

    def get_initial(self):
        initial = super().get_initial()
        # Si el mensaje es una respuesta, pre-rellena el destinatario y el asunto
        reply_to_pk = self.request.GET.get('reply_to')
        if reply_to_pk:
            original_message = get_object_or_404(Message, pk=reply_to_pk)
            initial['receiver'] = original_message.sender
            if not original_message.subject.startswith('Re:'):
                initial['subject'] = f'Re: {original_message.subject}'
            else:
                initial['subject'] = original_message.subject
        return initial

    def form_valid(self, form):
        form.instance.sender = self.request.user # Asigna el remitente actual
        messages.success(self.request, '¡Mensaje enviado exitosamente!')
        return super().form_valid(form)