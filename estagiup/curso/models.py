from django.db import models

class Curso(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Curso")
    instituicao = models.ForeignKey('instituicao.Instituicao', on_delete=models.SET_NULL, related_name='cursos', blank=True, null=True, verbose_name="Instituição Ofertante")
    nivel = models.CharField(max_length=50, verbose_name="Nível do Curso")

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.nome
