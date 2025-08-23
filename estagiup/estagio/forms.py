from django import forms
from .models import Estagio

class EstagioForm(forms.ModelForm):
    """
    Formulário para o cadastro de um novo estágio.
    """
    class Meta:
        model = Estagio
        fields = ['dt_ini', 'dt_fim', 'status', 'nota', 'supervisor', 'orientador']
        widgets = {
            'dt_ini': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'dt_fim': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nota': forms.NumberInput(attrs={'class': 'form-control'}),
            'supervisor': forms.Select(attrs={'class': 'form-control'}),
            'orientador': forms.Select(attrs={'class': 'form-control'}),
        }
