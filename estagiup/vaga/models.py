from django.db import models

class Vaga(models.Model):
    """
    Modelo para representar uma oportunidade de estágio ou trabalho.
    """
    titulo = models.CharField(max_length=255, verbose_name="Título da Vaga")
    descricao = models.TextField(verbose_name="Descrição da Vaga")
    # Associa a Vaga a uma Instituição (relação N:1)
    instituicao = models.ForeignKey('instituicao.Instituicao', on_delete=models.CASCADE, related_name='vagas', verbose_name="Instituição")
    numVagas = models.IntegerField(verbose_name="Número de Vagas")
    prazo = models.DateField(verbose_name="Prazo de Inscrição")
    # Associa a Vaga a múltiplos Cursos (relação N:N)
    cursos = models.ManyToManyField('curso.Curso', related_name='vagas_relacionadas', verbose_name="Cursos Relacionados")

    class Meta:
        verbose_name = "Vaga"
        verbose_name_plural = "Vagas"

    def __str__(self):
        return self.titulo