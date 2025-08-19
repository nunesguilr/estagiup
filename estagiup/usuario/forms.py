from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import PerfilUsuario, Instituicao, Curso

class UserRegistrationForm(UserCreationForm):
    """
    Formulário de criação de utilizador com campos extras para o PerfilUsuario e para escolher o grupo.
    """
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Escolha um grupo",
        label="Grupo",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Campos de endereço composto
    rua = forms.CharField(max_length=255, label="Rua", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    bairro = forms.CharField(max_length=100, label="Bairro", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cidade = forms.CharField(max_length=100, label="Cidade", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    estado = forms.CharField(max_length=50, label="Estado", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    pais = forms.CharField(max_length=50, label="País", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    # Outros campos do modelo PerfilUsuario
    telefone = forms.CharField(max_length=20, label="Telefone", widget=forms.TextInput(attrs={'class': 'form-control'}))
    cpf = forms.CharField(max_length=14, label="CPF", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    data_nascimento = forms.DateField(label="Data de Nascimento", required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    genero = forms.ChoiceField(choices=PerfilUsuario.GENERO_CHOICES, label="Gênero", required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    descricao = forms.CharField(label="Descrição", required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    instituicao = forms.ModelChoiceField(queryset=Instituicao.objects.all(), label="Instituição", required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    curso = forms.ModelChoiceField(queryset=Curso.objects.all(), label="Curso", required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            PerfilUsuario.objects.create(
                user=user,
                rua=self.cleaned_data['rua'],
                bairro=self.cleaned_data['bairro'],
                cidade=self.cleaned_data['cidade'],
                estado=self.cleaned_data['estado'],
                pais=self.cleaned_data['pais'],
                telefone=self.cleaned_data['telefone'],
                cpf=self.cleaned_data['cpf'],
                data_nascimento=self.cleaned_data['data_nascimento'],
                genero=self.cleaned_data['genero'],
                descricao=self.cleaned_data['descricao'],
                instituicao=self.cleaned_data['instituicao'],
                curso=self.cleaned_data['curso'],
            )
            group = self.cleaned_data['group']
            user.groups.add(group)
        return user