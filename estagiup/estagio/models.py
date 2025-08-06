from django.db import models
from usuario.models import PerfilUsuario
from vaga.models import Vaga

class Estagio(models.Model):
    aluno = models.OneToOneField(PerfilUsuario, on_delete=models.CASCADE, related_name='estagio_realizado', verbose_name="Aluno")
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE, related_name='estagios_associados', verbose_name="Vaga")
    supervisor = models.ForeignKey(PerfilUsuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='estagios_supervisionados', verbose_name="Supervisor")
    orientador = models.ForeignKey(PerfilUsuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='estagios_orientados', verbose_name="Orientador")
    dt_ini = models.DateField(verbose_name="Data de Início")
    dt_fim = models.DateField(verbose_name="Data de Fim")
    status = models.BooleanField(default=False, verbose_name="Estágio Ativo")
    nota = models.FloatField(null=True, blank=True, verbose_name="Nota do Estágio")

    class Meta:
        verbose_name = "Estágio"
        verbose_name_plural = "Estágios"

    def __str__(self):
        return f"Estágio de {self.aluno.user.username} na vaga {self.vaga.titulo}"
