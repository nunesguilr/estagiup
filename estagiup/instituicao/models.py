from django.db import models
from usuario.models import PerfilUsuario

class Instituicao(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome da Instituição")
    endereco = models.CharField(max_length=255, verbose_name="Endereço")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ")
    responsaveis = models.ManyToManyField(PerfilUsuario, related_name='instituicoes_responsavel', verbose_name="Responsáveis")
    status = models.BooleanField(default=True, verbose_name="Status Ativo")

    class Meta:
        verbose_name = "Instituição"
        verbose_name_plural = "Instituições"

    def __str__(self):
        return self.nome