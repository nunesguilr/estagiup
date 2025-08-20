from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from usuario.models import PerfilUsuario
from datetime import date

class Command(BaseCommand):
    help = 'Cria utilizadores de desenvolvimento com dados de perfil completos para cada grupo.'

    def handle(self, *args, **options):
        # Dicionário de utilizadores de desenvolvimento com dados de perfil completos
        dev_users_data = [
            {
                'username': 'aluno_dev', 
                'email': 'aluno@estagiup.com', 
                'password': 'devpassword', 
                'group': 'Alunos',
                'perfil': {
                    'rua': 'Rua do Aluno, 123',
                    'bairro': 'Bairro do Aluno',
                    'cidade': 'Guanambi',
                    'estado': 'Bahia',
                    'pais': 'Brasil',
                    'telefone': '77991234567',
                    'cpf': '111.111.111-11',
                    'data_nascimento': date(2000, 1, 1),
                    'genero': 'masculino',
                    'descricao': 'Utilizador de teste com perfil de aluno.',
                }
            },
            {
                'username': 'responsavel_dev', 
                'email': 'responsavel@estagiup.com', 
                'password': 'devpassword', 
                'group': 'Responsaveis da Instituicao',
                'perfil': {
                    'rua': 'Avenida da Empresa, 456',
                    'bairro': 'Centro',
                    'cidade': 'São Paulo',
                    'estado': 'São Paulo',
                    'pais': 'Brasil',
                    'telefone': '11987654321',
                    'cpf': '222.222.222-22',
                    'data_nascimento': date(1985, 5, 10),
                    'genero': 'feminino',
                    'descricao': 'Utilizador de teste com perfil de responsável de instituição.',
                }
            },
            {
                'username': 'supervisor_dev', 
                'email': 'supervisor@estagiup.com', 
                'password': 'devpassword', 
                'group': 'Supervisores',
                'perfil': {
                    'rua': 'Rua do Supervisor, 789',
                    'bairro': 'Zona Industrial',
                    'cidade': 'Porto',
                    'estado': 'Porto',
                    'pais': 'Portugal',
                    'telefone': '221234567',
                    'cpf': '333.333.333-33',
                    'data_nascimento': date(1978, 8, 20),
                    'genero': 'nao_informado',
                    'descricao': 'Utilizador de teste com perfil de supervisor.',
                }
            },
            {
                'username': 'orientador_dev', 
                'email': 'orientador@estagiup.com', 
                'password': 'devpassword', 
                'group': 'Orientadores',
                'perfil': {
                    'rua': 'Rua do Orientador, 101',
                    'bairro': 'Campus Universitário',
                    'cidade': 'Coimbra',
                    'estado': 'Coimbra',
                    'pais': 'Portugal',
                    'telefone': '319876543',
                    'cpf': '444.444.444-44',
                    'data_nascimento': date(1980, 3, 15),
                    'genero': 'masculino',
                    'descricao': 'Utilizador de teste com perfil de orientador.',
                }
            },
        ]

        for user_data in dev_users_data:
            username = user_data['username']
            email = user_data['email']
            password = user_data['password']
            group_name = user_data['group']
            perfil_data = user_data['perfil']

            try:
                user = User.objects.get(username=username)
                self.stdout.write(self.style.WARNING(f"Utilizador '{username}' já existe. Nenhuma ação foi necessária."))
                # Tenta criar o perfil se o utilizador já existe mas não tem perfil.
                if not hasattr(user, 'perfil'):
                    PerfilUsuario.objects.create(user=user, **perfil_data)
                    self.stdout.write(self.style.SUCCESS(f"  - Perfil de utilizador criado para '{username}'."))
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write(self.style.SUCCESS(f"Utilizador '{username}' criado com sucesso."))
                self.stdout.write(self.style.WARNING(f"  - Palavra-passe: {password}"))
                
                PerfilUsuario.objects.create(user=user, **perfil_data)
                self.stdout.write(self.style.SUCCESS(f"  - Perfil de utilizador criado para '{username}'."))
            
            try:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
                self.stdout.write(self.style.SUCCESS(f"  - Utilizador '{username}' adicionado ao grupo '{group_name}'."))
            except Group.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"  - Grupo '{group_name}' não encontrado. O utilizador '{username}' não foi atribuído a este grupo."))

        self.stdout.write(self.style.SUCCESS("\nProcesso de criação de utilizadores de desenvolvimento concluído."))
