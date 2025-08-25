from django import forms
from .models import Instituicao

class InstituicaoForm(forms.ModelForm):
    """
    Formulário para o cadastro de uma nova instituição, sem a seleção manual de responsáveis.
    """
    class Meta:
        model = Instituicao
        exclude = ['responsaveis'] # Adicione esta linha
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
