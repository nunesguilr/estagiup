from django.db import models

class Notificacao(models.Model):
    mensagem = models.TextField()
    destinatario = models.ForeignKey('contas.Usuario', on_delete=models.CASCADE)
    data_envio = models.DateTimeField(auto_now_add=True)
    lido = models.BooleanField(default=False)
    tipo = models.CharField(
        max_length=50,
        choices=[('geral', 'Geral'), ('alerta', 'Alerta'), ('aviso', 'Aviso')],
        default='geral'
    )  

    def __str__(self):
        return f"Notificação para {self.destinatario.nome}"