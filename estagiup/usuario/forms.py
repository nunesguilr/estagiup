from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group
from .models import PerfilUsuario  # Importa apenas PerfilUsuario do seu app
from instituicao.models import Instituicao  # Importa diretamente do app instituicao
from curso.models import Curso  # Importa diretamente do app curso

class PerfilUpdateForm(forms.ModelForm):
    """
    Formulário para atualizar os dados do PerfilUsuario.
    """
    class Meta:
        model = PerfilUsuario
        exclude = ('user',)
        widgets = {
            'rua': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'instituicao': forms.Select(attrs={'class': 'form-control'}),
            'curso': forms.Select(attrs={'class': 'form-control'}),
        }
    
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

    rua = forms.CharField(max_length=255, label="Rua", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    bairro = forms.CharField(max_length=100, label="Bairro", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cidade = forms.CharField(max_length=100, label="Cidade", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    estado = forms.CharField(max_length=50, label="Estado", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    pais = forms.CharField(max_length=50, label="País", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Este loop passa por todos os campos do formulário
        for field_name, field in self.fields.items():
            # E adiciona a classe de estilo do Bootstrap em cada um
            field.widget.attrs['class'] = 'form-control form-control-glass'
            # Adiciona placeholders baseados nos labels
            if field.label:
                field.widget.attrs['placeholder'] = field.label    

        if self.errors:
            for field_name in self.errors:
                if field_name in self.fields:
                    self.fields[field_name].widget.attrs['class'] += ' is-invalid'

class UserAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adiciona as classes de estilo e placeholders
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control form-control-glass', 'placeholder': 'Nome de Usuário'}
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control form-control-glass', 'placeholder': 'Senha'}
        )