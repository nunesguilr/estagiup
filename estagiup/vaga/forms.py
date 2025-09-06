from django import forms
from .models import Vaga
from instituicao.models import Instituicao

class VagaForm(forms.ModelForm):
    """
    Formulário para o cadastro de uma nova vaga.
    """
    instituicao = forms.ModelChoiceField(
        queryset=Instituicao.objects.none(),
        label="Instituição Ofertante",
        required=True
    )
    
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # Filtra as instituições com base no utilizador logado
            # Acede aos campos de utilizador diretamente, sem o .perfil
            self.fields['instituicao'].queryset = Instituicao.objects.filter(responsaveis=user)
