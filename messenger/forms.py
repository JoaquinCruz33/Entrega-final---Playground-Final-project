from django import forms
from .models import Message
from django.contrib.auth.models import User

class MessageForm(forms.ModelForm):
    # Puedes limitar los destinatarios a usuarios existentes si es necesario
    # Por ejemplo, si quieres que solo se puedan enviar mensajes a usuarios activos
    receiver = forms.ModelChoiceField(queryset=User.objects.all().order_by('username'), label="Destinatario")

    class Meta:
        model = Message
        fields = ['receiver', 'subject', 'body']