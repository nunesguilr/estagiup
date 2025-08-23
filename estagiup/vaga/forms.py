from django import forms
from .models import Vaga

class VagaForm(forms.ModelForm):
    """
    Formulário para o cadastro de uma nova vaga.
    """
    class Meta:
        model = Vaga
        fields = ['titulo', 'descricao', 'instituicao', 'numVagas', 'prazo', 'cursos']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'instituicao': forms.Select(attrs={'class': 'form-control'}),
            'numVagas': forms.NumberInput(attrs={'class': 'form-control'}),
            'prazo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cursos': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }