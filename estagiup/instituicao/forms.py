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


class InstituicaoForm(forms.ModelForm):
    class Meta:
        model = Instituicao
        fields = '__all__' # ou a lista de campos que você usa

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona a classe 'form-control-glass' a todos os campos
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control form-control-glass'
            })

         # Remove a classe padrão de campos de texto do checkbox e adiciona a correta
        self.fields['status'].widget.attrs.pop('class', None)
        self.fields['status'].widget.attrs.update({
            'class': 'form-check-input'
        })

        # Adiciona a descrição para o campo status
        self.fields['status'].help_text = 'Selecione para tornar a instituição ativa no sistema (Caso contrario, não será exibida nas buscas para Estagios).'
