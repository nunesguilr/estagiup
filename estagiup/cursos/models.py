from django.db import models

class Curso(models.Model):
    nome = models.CharField(max_length=255)
    instituicao = models.ForeignKey('contas.ContaInstituicao', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome