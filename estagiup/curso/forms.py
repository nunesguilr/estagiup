from django import forms
from .models import Curso
from instituicao.models import Instituicao

class CursoForm(forms.ModelForm):
    # O campo 'inst' agora é um ModelChoiceField para criar um menu suspenso
    inst = forms.ModelChoiceField(
        queryset=Instituicao.objects.all(),
        label="Instituição Ofertante",
        required=True
    )

    class Meta:
        model = Curso
        fields = ['nome', 'inst', 'nivel']
        
    def __init__(self, *args, **kwargs):
        # Passa a lista de instituições disponíveis para o formulário
        instituicoes_disponiveis = kwargs.pop('instituicoes', None)
        super().__init__(*args, **kwargs)
        
        # Filtra o queryset do campo 'inst' com base na lista de instituições passadas
        if instituicoes_disponiveis is not None:
            self.fields['inst'].queryset = instituicoes_disponiveis

        # Estilização dos campos do formulário
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
