from django import forms
from .models import Notificacao

class NotificacaoForm(forms.ModelForm):
    class Meta:
        model = Notificacao
        fields = ['mensagem', 'destinatario', 'lido', 'tipo']