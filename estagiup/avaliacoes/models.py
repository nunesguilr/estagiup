from django.db import models

class Nota(models.Model):
    estagio = models.ForeignKey('estagios.Estagio', on_delete=models.CASCADE)
    valor = models.FloatField()
    comentario = models.TextField(blank=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Nota {self.valor} - Estágio {self.estagio.id}"

class Relatorio(models.Model):
    estagio = models.ForeignKey('estagios.Estagio', on_delete=models.CASCADE)
    conteudo = models.TextField()  
    data_envio = models.DateTimeField(auto_now_add=True)
    validade = models.DateField()
    avaliacao = models.FloatField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('rascunho', 'Rascunho'), ('enviado', 'Enviado'), ('avaliado', 'Avaliado')],
        default='rascunho'
    )
    versao = models.IntegerField(default=1)

    def __str__(self):
        return f"Relatório - Estágio {self.estagio.id} (Versão {self.versao})"