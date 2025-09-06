from django.db import models
from usuario.models import Usuario

class Instituicao(models.Model):
    # Opções para o tipo de instituição
    TIPO_INSTITUICAO_CHOICES = (
        ('empresa', 'Empresa'),
        ('instituicao_ensino', 'Instituição de Ensino'),
    )

    nome = models.CharField(max_length=255, verbose_name="Nome da Instituição")
    # Endereço composto
    rua = models.CharField(max_length=255, verbose_name="Rua", blank=True, null=True)
    bairro = models.CharField(max_length=100, verbose_name="Bairro", blank=True, null=True)
    cidade = models.CharField(max_length=100, verbose_name="Cidade", blank=True, null=True)
    estado = models.CharField(max_length=50, verbose_name="Estado", blank=True, null=True)
    pais = models.CharField(max_length=50, verbose_name="País", blank=True, null=True)
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ")
    responsaveis = models.ManyToManyField('usuario.Usuario', related_name='instituicoes_responsavel', verbose_name="Responsáveis", blank=True)
    status = models.BooleanField(default=True, verbose_name="Status Ativo")
    tipo = models.CharField(max_length=20, choices=TIPO_INSTITUICAO_CHOICES, default='empresa', verbose_name="Tipo de Instituição")

    class Meta:
        verbose_name = "Instituição"
        verbose_name_plural = "Instituições"

    def __str__(self):
        return self.nome
