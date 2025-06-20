from django import forms
from .models import Nota, Relatorio

class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['estagio', 'valor', 'comentario']

class RelatorioForm(forms.ModelForm):
    class Meta:
        model = Relatorio
        fields = ['estagio', 'conteudo', 'validade']
