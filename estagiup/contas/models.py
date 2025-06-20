# contas/models.py
from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    tipo_usuario = models.CharField(
        max_length=20,
        choices=[
            ('aluno', 'Aluno'),
            ('empresa', 'Empresa'),
            ('professor', 'Professor'),
            ('supervisor', 'Supervisor'),
            ('instituicao', 'Instituição')
        ],
        default='aluno'
    )
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Aluno(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    matricula = models.CharField(max_length=50, unique=True)
    curso = models.ForeignKey('cursos.Curso', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.nome} - {self.matricula}"

class ContaEmpresa(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    nome_empresa = models.CharField(max_length=255)
    nivel_permissao = models.CharField(
        max_length=10,
        choices=[('basico', 'Básico'), ('avancado', 'Avançado')],
        default='basico'
    )
    localizacao = models.CharField(max_length=255)

    def __str__(self):
        return self.nome_empresa

class Supervisor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    cargo = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.usuario.nome} - {self.cargo}"

class Professor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.usuario.nome

class ContaInstituicao(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    nome_instituicao = models.CharField(max_length=255)

    def __str__(self):
        return self.nome_instituicao