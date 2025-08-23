from django import forms
from .models import Curso

class CursoForm(forms.ModelForm):
    """
    Formulário para o cadastro de um novo curso.
    """
    class Meta:
        model = Curso
        fields = ['nome', 'inst', 'nivel']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'inst': forms.TextInput(attrs={'class': 'form-control'}),
            'nivel': forms.TextInput(attrs={'class': 'form-control'}),
        }