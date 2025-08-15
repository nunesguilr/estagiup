from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_usuario')
    endereco = models.CharField(max_length=100, verbose_name="endereco")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")

    class Meta:
        verbose_name = "Perfil do Usuário"
        verbose_name_plural = "Perfis dos Usuários"

    def __str__(self):
        return self.user.username