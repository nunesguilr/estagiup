from django.db import models

class Vaga(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    localizacao = models.CharField(max_length=255)
    requisitos = models.TextField()
    empresa = models.ForeignKey('contas.ContaEmpresa', on_delete=models.CASCADE)
    data_publicacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo