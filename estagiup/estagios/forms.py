from django import forms
from .models import Estagio

class EstagioForm(forms.ModelForm):
    class Meta:
        model = Estagio
        fields = ['aluno', 'vaga', 'supervisor', 'professor', 'data_inicio', 'data_fim', 'carga_horaria', 'status']
