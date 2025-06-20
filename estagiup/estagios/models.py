from django.db import models

class Estagio(models.Model):
    aluno = models.ForeignKey('contas.Aluno', on_delete=models.CASCADE)
    vaga = models.ForeignKey('vagas.Vaga', on_delete=models.CASCADE)
    supervisor = models.ForeignKey('contas.Supervisor', on_delete=models.SET_NULL, null=True, blank=True)
    professor = models.ForeignKey('contas.Professor', on_delete=models.SET_NULL, null=True, blank=True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    carga_horaria = models.IntegerField()  
    status = models.CharField(
        max_length=20,
        choices=[('ativo', 'Ativo'), ('concluido', 'Concluído'), ('cancelado', 'Cancelado')],
        default='ativo'
    )

    def __str__(self):
        return f"Estágio de {self.aluno.usuario.nome} - {self.vaga.titulo}"