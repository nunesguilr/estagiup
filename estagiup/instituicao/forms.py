from django import forms
from .models import Instituicao

class InstituicaoForm(forms.ModelForm):
    """
    Formulário para o cadastro e edição de uma instituição, sem a seleção manual de responsáveis.
    """
    class Meta:
        model = Instituicao
        exclude = ['responsaveis']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'rua': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona a classe 'form-control-glass' a todos os campos de texto
        for field in self.fields.values():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.Select)):
                field.widget.attrs.update({
                    'class': 'form-control form-control-glass'
                })
        
        # Corrige a classe do checkbox
        if 'status' in self.fields:
            self.fields['status'].widget.attrs.update({
                'class': 'form-check-input'
            })
            self.fields['status'].help_text = 'Selecione para tornar a instituição ativa no sistema.'
