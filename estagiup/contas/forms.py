from django import forms
from .models import Usuario, Aluno, ContaEmpresa, Supervisor, Professor, ContaInstituicao

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'tipo_usuario']

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['usuario', 'matricula', 'curso']

class ContaEmpresaForm(forms.ModelForm):
    class Meta:
        model = ContaEmpresa
        fields = ['usuario', 'nome_empresa', 'nivel_permissao', 'localizacao']

class SupervisorForm(forms.ModelForm):
    class Meta:
        model = Supervisor
        fields = ['usuario', 'cargo']

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['usuario']

class ContaInstituicaoForm(forms.ModelForm):
    class Meta:
        model = ContaInstituicao
        fields = ['usuario', 'nome_instituicao']
