from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(User):
    # Opções para o gênero
    GENERO_CHOICES = (
        ('masculino', 'Masculino'),
        ('feminino', 'Feminino'),
        ('nao_informado', 'Não Informado'),
    )

    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    
    curso = models.ForeignKey('curso.Curso', on_delete=models.SET_NULL, related_name='alunos', blank=True, null=True, verbose_name="Curso")
    # Endereço composto
    rua = models.CharField(max_length=255, verbose_name="Rua", blank=True, null=True)
    bairro = models.CharField(max_length=100, verbose_name="Bairro", blank=True, null=True)
    cidade = models.CharField(max_length=100, verbose_name="Cidade", blank=True, null=True)
    estado = models.CharField(max_length=50, verbose_name="Estado", blank=True, null=True)
    pais = models.CharField(max_length=50, verbose_name="País", blank=True, null=True)

    telefone = models.CharField(max_length=20, verbose_name="Telefone", blank=True, null=True)
    cpf = models.CharField(max_length=14, verbose_name="CPF", blank=True, null=True)
    data_nascimento = models.DateField(verbose_name="Data de Nascimento", blank=True, null=True)
    genero = models.CharField(max_length=20, choices=GENERO_CHOICES, default='nao_informado', verbose_name="Gênero")
    descricao = models.TextField(verbose_name="Descrição", blank=True, null=True)
    
    # Relações com outros modelos usando string para evitar circular import
    # instituicao = models.ForeignKey('instituicao.Instituicao', on_delete=models.SET_NULL, related_name='membros', blank=True, null=True, verbose_name="Instituição")


    class Meta:
        verbose_name = "Perfil do Usuário"
        verbose_name_plural = "Perfis dos Usuários"

    def __str__(self):
        return self.user.username
