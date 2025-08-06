from django.db import models

class Curso(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Curso")
    inst = models.CharField(max_length=255, verbose_name="Instituição Ofertante")
    nivel = models.CharField(max_length=50, verbose_name="Nível do Curso")

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.nome
