from django.db import models
from instituicao.models import Instituicao
from curso.models import Curso

class Vaga(models.Model):
    titulo = models.CharField(max_length=255, verbose_name="Título da Vaga")
    descricao = models.TextField(verbose_name="Descrição da Vaga")
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE, related_name='vagas', verbose_name="Instituição")
    numVagas = models.IntegerField(verbose_name="Número de Vagas")
    prazo = models.DateField(verbose_name="Prazo de Inscrição")
    cursos = models.ManyToManyField(Curso, related_name='vagas_relacionadas', verbose_name="Cursos Relacionados")

    class Meta:
        verbose_name = "Vaga"
        verbose_name_plural = "Vagas"

    def __str__(self):
        return self.titulo
