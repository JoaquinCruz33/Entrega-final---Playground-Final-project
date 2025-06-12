from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE, verbose_name="Remitente")
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE, verbose_name="Destinatario")
    subject = models.CharField(max_length=200, verbose_name="Asunto")
    body = models.TextField(verbose_name="Cuerpo del Mensaje")
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Envío")
    is_read = models.BooleanField(default=False, verbose_name="Leído")

    class Meta:
        ordering = ['-sent_at'] # Ordenar por fecha de envío descendente

    def __str__(self):
        return f'De {self.sender.username} a {self.receiver.username}: {self.subject}'

    def get_absolute_url(self):
        return reverse('message_detail', kwargs={'pk': self.pk})