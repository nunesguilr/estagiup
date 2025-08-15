from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import PerfilUsuario

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

    endereco = forms.CharField(max_length=100, label="Endereço", widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefone = forms.CharField(max_length=20, label="Telefone", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        """
        Sobrescreve o método save para criar o PerfilUsuario e atribuir o grupo.
        A lógica de criação do User é tratada pela classe pai (UserCreationForm).
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Cria o PerfilUsuario associado
            PerfilUsuario.objects.create(
                user=user,
                endereco=self.cleaned_data['endereco'],
                telefone=self.cleaned_data['telefone']
            )
            # Atribui o utilizador ao grupo selecionado
            group = self.cleaned_data['group']
            user.groups.add(group)
        return user
