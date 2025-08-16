from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Cria um utilizador administrador para o ambiente de desenvolvimento.'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin'

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f"Utilizador de administração '{username}' criado com sucesso."))
            self.stdout.write(self.style.WARNING("Palavra-passe: admin"))
        else:
            self.stdout.write(self.style.WARNING(f"O utilizador de administração '{username}' já existe. Nenhuma ação foi necessária."))