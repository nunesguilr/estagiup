# usuario/management/commands/initial_setup.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, transaction, connection
from datetime import date, timedelta
import sys
import random

# Importa todos os modelos do projeto
from usuario.models import PerfilUsuario
from instituicao.models import Instituicao
from vaga.models import Vaga
from curso.models import Curso
from estagio.models import Estagio

class Command(BaseCommand):
    help = 'Executa o setup inicial do projeto, criando grupos, permissões, usuários de teste e dados de exemplo.'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.courses = {}
        self.institutions = {}
        self.users = {}
        self.vagas = {}

    def handle(self, *args, **options):
        # Verificar se as migrações foram aplicadas
        if not self._check_migrations_applied():
            self.stdout.write(self.style.ERROR(
                "Erro: Migrações do Django não foram aplicadas. "
                "Execute 'python manage.py migrate' primeiro."
            ))
            sys.exit(1)
            
        self.stdout.write(self.style.SUCCESS("Iniciando o setup inicial do projeto Estagiup..."))

        try:
            with transaction.atomic():
                self._setup_groups_and_permissions()
                self._setup_admin_user()
                self._setup_institutions_and_courses()
                self._setup_dev_users()
                self._setup_vagas()
                self._setup_estagios()
            
            self.stdout.write(self.style.SUCCESS("\nSetup inicial concluído com sucesso!"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro durante o setup: {str(e)}"))
            raise

    def _check_migrations_applied(self):
        """Verifica se as migrações básicas do Django foram aplicadas"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_group'")
                return cursor.fetchone() is not None
        except:
            return False

    def _setup_groups_and_permissions(self):
        """Configura grupos e permissões"""
        self.stdout.write(self.style.SUCCESS("\n--- Criando Grupos e Permissões ---"))
        
        groups_permissions_map = {
            'Alunos': [
                ('view_perfilusuario', PerfilUsuario),
                ('change_perfilusuario', PerfilUsuario),
                ('view_vaga', Vaga),
                ('view_curso', Curso),
                ('view_estagio', Estagio),
                ('view_instituicao', Instituicao),
                ('add_estagio', Estagio),
            ],
            'Responsaveis da Instituicao': [
                ('view_instituicao', Instituicao),
                ('change_instituicao', Instituicao),
                ('add_instituicao', Instituicao),
                ('delete_instituicao', Instituicao),
                ('view_vaga', Vaga),
                ('add_vaga', Vaga),
                ('change_vaga', Vaga),
                ('delete_vaga', Vaga),
                ('view_estagio', Estagio),
                ('view_perfilusuario', PerfilUsuario),
            ],
            'Supervisores': [
                ('view_estagio', Estagio),
                ('change_estagio', Estagio),
                ('view_perfilusuario', PerfilUsuario),
                ('view_instituicao', Instituicao),
                ('view_vaga', Vaga),
            ],
            'Orientadores': [
                ('view_estagio', Estagio),
                ('view_perfilusuario', PerfilUsuario),
            ],
        }

        def get_permission(codename, model):
            try:
                content_type = ContentType.objects.get_for_model(model)
                return Permission.objects.get(codename=codename, content_type=content_type)
            except (ContentType.DoesNotExist, Permission.DoesNotExist):
                return None

        for group_name, permissions_list in groups_permissions_map.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Grupo '{group.name}' criado com sucesso."))
            else:
                self.stdout.write(self.style.WARNING(f"Grupo '{group.name}' já existe."))
            
            for codename, model in permissions_list:
                perm = get_permission(codename, model)
                if perm:
                    try:
                        group.permissions.add(perm)
                    except IntegrityError:
                        pass
                else:
                    self.stdout.write(self.style.WARNING(
                        f"Permissão '{codename}' para {model.__name__} não encontrada"
                    ))
        
        self.stdout.write(self.style.SUCCESS("Processo de grupos e permissões concluído."))

    def _setup_admin_user(self):
        """Configura usuário admin"""
        self.stdout.write(self.style.SUCCESS("\n--- Criando Admin de Desenvolvimento ---"))
        
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin'

        if not User.objects.filter(username=username).exists():
            admin_user = User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f"Admin '{username}' criado com sucesso."))
            self.stdout.write(self.style.WARNING(f"Palavra-passe: {password}"))
        else:
            self.stdout.write(self.style.WARNING(f"Admin '{username}' já existe."))

    def _setup_institutions_and_courses(self):
        """Configura instituições e cursos"""
        self.stdout.write(self.style.SUCCESS("\n--- Criando Cursos de Desenvolvimento ---"))
        
        courses_data = [
            {'nome': 'Ciência da Computação', 'inst': 'Universidade Federal', 'nivel': 'Graduação'},
            {'nome': 'Engenharia de Software', 'inst': 'Faculdade Tecnológica', 'nivel': 'Graduação'},
            {'nome': 'Administração', 'inst': 'Universidade Federal', 'nivel': 'Graduação'},
            {'nome': 'Sistemas de Informação', 'inst': 'Faculdade Tecnológica', 'nivel': 'Graduação'},
            {'nome': 'Análise e Desenvolvimento de Sistemas', 'inst': 'Instituto Tecnológico', 'nivel': 'Tecnólogo'},
            {'nome': 'Psicologia', 'inst': 'Universidade Federal', 'nivel': 'Graduação'},
            {'nome': 'Direito', 'inst': 'Faculdade de Direito', 'nivel': 'Graduação'},
        ]
        
        for course_data in courses_data:
            course, created = Curso.objects.get_or_create(
                nome=course_data['nome'],
                defaults={'inst': course_data['inst'], 'nivel': course_data['nivel']}
            )
            self.courses[course.nome] = course
            if created:
                self.stdout.write(self.style.SUCCESS(f"Curso '{course.nome}' criado com sucesso."))
            else:
                self.stdout.write(self.style.WARNING(f"Curso '{course.nome}' já existe."))

        self.stdout.write(self.style.SUCCESS("\n--- Criando Instituições de Desenvolvimento ---"))
        
        institutions_data = [
            {'nome': 'Tech Solutions', 'cnpj': '12.345.678/0001-00', 'endereco': 'Avenida Tecnologia, 100', 'telefone': '21987654321', 'tipo': 'empresa'},
            {'nome': 'Inovação Digital', 'cnpj': '23.456.789/0001-11', 'endereco': 'Rua da Inovação, 200', 'telefone': '1133445566', 'tipo': 'empresa'},
            {'nome': 'Universidade Federal', 'cnpj': '34.567.890/0001-22', 'endereco': 'Campus Universitário, s/n', 'telefone': '1155667788', 'tipo': 'instituicao_ensino'},
            {'nome': 'Faculdade Tecnológica', 'cnpj': '45.678.901/0001-33', 'endereco': 'Avenida do Conhecimento, 300', 'telefone': '1199887766', 'tipo': 'instituicao_ensino'},
            {'nome': 'Banco Central', 'cnpj': '56.789.012/0001-44', 'endereco': 'Praça da Economia, 50', 'telefone': '1122334455', 'tipo': 'empresa'},
            {'nome': 'Hospital Geral', 'cnpj': '67.890.123/0001-55', 'endereco': 'Rua da Saúde, 400', 'telefone': '1144556677', 'tipo': 'empresa'},
        ]
        
        for inst_data in institutions_data:
            inst, created = Instituicao.objects.get_or_create(
                cnpj=inst_data['cnpj'],
                defaults={
                    'nome': inst_data['nome'], 
                    'endereco': inst_data['endereco'], 
                    'telefone': inst_data['telefone'], 
                    'tipo': inst_data['tipo']
                }
            )
            self.institutions[inst.nome] = inst
            if created:
                self.stdout.write(self.style.SUCCESS(f"Instituição '{inst.nome}' criada com sucesso."))
            else:
                self.stdout.write(self.style.WARNING(f"Instituição '{inst.nome}' já existe."))

    def _setup_dev_users(self):
        """Configura usuários de desenvolvimento"""
        self.stdout.write(self.style.SUCCESS("\n--- Criando Utilizadores de Desenvolvimento ---"))
        
        dev_users_data = [
            {
                'username': 'aluno1', 'email': 'aluno1@estagiup.com', 'password': 'devpassword',
                'group': 'Alunos', 'is_staff': False,
                'perfil_data': {
                    'rua': 'Rua do Estudante, 123', 'bairro': 'Centro', 'cidade': 'São Paulo', 
                    'estado': 'SP', 'pais': 'Brasil', 'telefone': '11987654321', 
                    'cpf': '111.111.111-11', 'data_nascimento': date(2000, 1, 1), 
                    'genero': 'masculino', 'descricao': 'Aluno dedicado de Ciência da Computação.',
                    'instituicao': self.institutions['Universidade Federal'],
                    'curso': self.courses['Ciência da Computação']
                }
            },
            {
                'username': 'aluno2', 'email': 'aluno2@estagiup.com', 'password': 'devpassword',
                'group': 'Alunos', 'is_staff': False,
                'perfil_data': {
                    'rua': 'Avenida do Conhecimento, 456', 'bairro': 'Universitário', 'cidade': 'Rio de Janeiro', 
                    'estado': 'RJ', 'pais': 'Brasil', 'telefone': '21987654321', 
                    'cpf': '222.222.222-22', 'data_nascimento': date(2001, 5, 15), 
                    'genero': 'feminino', 'descricao': 'Aluna de Engenharia de Software.',
                    'instituicao': self.institutions['Faculdade Tecnológica'],
                    'curso': self.courses['Engenharia de Software']
                }
            },
            {
                'username': 'responsavel1', 'email': 'responsavel1@estagiup.com', 'password': 'devpassword',
                'group': 'Responsaveis da Instituicao', 'is_staff': True,
                'perfil_data': {
                    'rua': 'Avenida Corporativa, 789', 'bairro': 'Financeiro', 'cidade': 'São Paulo', 
                    'estado': 'SP', 'pais': 'Brasil', 'telefone': '1199887766', 
                    'cpf': '333.333.333-33', 'data_nascimento': date(1980, 3, 10), 
                    'genero': 'masculino', 'descricao': 'Gerente de RH da Tech Solutions.',
                    'instituicao': self.institutions['Tech Solutions'],
                    'curso': self.courses['Administração']
                }
            },
            {
                'username': 'supervisor1', 'email': 'supervisor1@estagiup.com', 'password': 'devpassword',
                'group': 'Supervisores', 'is_staff': True,
                'perfil_data': {
                    'rua': 'Rua da Liderança, 101', 'bairro': 'Gerencial', 'cidade': 'Rio de Janeiro', 
                    'estado': 'RJ', 'pais': 'Brasil', 'telefone': '2199776655', 
                    'cpf': '444.444.444-44', 'data_nascimento': date(1975, 8, 20), 
                    'genero': 'feminino', 'descricao': 'Supervisora de Desenvolvimento.',
                    'instituicao': self.institutions['Tech Solutions']
                }
            },
            {
                'username': 'orientador1', 'email': 'orientador1@estagiup.com', 'password': 'devpassword',
                'group': 'Orientadores', 'is_staff': True,
                'perfil_data': {
                    'rua': 'Avenida Acadêmica, 202', 'bairro': 'Universitário', 'cidade': 'São Paulo', 
                    'estado': 'SP', 'pais': 'Brasil', 'telefone': '1199665544', 
                    'cpf': '555.555.555-55', 'data_nascimento': date(1970, 12, 5), 
                    'genero': 'masculino', 'descricao': 'Professor Orientador.',
                    'instituicao': self.institutions['Universidade Federal'],
                    'curso': self.courses['Ciência da Computação']
                }
            },
            {
                'username': 'aluno3', 'email': 'aluno3@estagiup.com', 'password': 'devpassword',
                'group': 'Alunos', 'is_staff': False,
                'perfil_data': {
                    'rua': 'Rua do Teste, 333', 'bairro': 'Teste', 'cidade': 'Guanambi', 'estado': 'Bahia', 'pais': 'Brasil',
                    'telefone': '7788776655', 'cpf': '666.666.666-66', 'data_nascimento': date(2002, 3, 20),
                    'genero': 'nao_informado', 'descricao': 'Aluno de Administração',
                    'instituicao': self.institutions['Universidade Federal'],
                    'curso': self.courses['Administração']
                }
            },
        ]

        self.users = {}
        for user_data in dev_users_data:
            user = self._create_dev_user(user_data)
            self.users[user.username] = user

    def _create_dev_user(self, user_data):
        """Cria um usuário de desenvolvimento"""
        username = user_data['username']
        
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': user_data['email'],
                'is_staff': user_data.get('is_staff', False),
                'password': 'devpassword' # Senha temporária, será definida em seguida
            }
        )
        
        if created:
            user.set_password(user_data['password'])
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Utilizador '{username}' criado com sucesso."))
        else:
            self.stdout.write(self.style.WARNING(f"Utilizador '{username}' já existe."))
        
        perfil_data = user_data['perfil_data']
        perfil, created = PerfilUsuario.objects.get_or_create(
            user=user, 
            defaults=perfil_data
        )
        
        if not created:
            for attr, value in perfil_data.items():
                setattr(perfil, attr, value)
            perfil.save()
        
        try:
            group = Group.objects.get(name=user_data['group'])
            user.groups.add(group)
            self.stdout.write(self.style.SUCCESS(f"  - Adicionado ao grupo: {user_data['group']}"))
        except Group.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"  - Grupo '{user_data['group']}' não encontrado."))
        
        return user
    
    def _setup_vagas(self):
        """Configura vagas de desenvolvimento"""
        self.stdout.write(self.style.SUCCESS("\n--- Criando Vagas de Desenvolvimento ---"))
        
        vagas_data = [
            {
                'titulo': 'Desenvolvedor Backend Python', 
                'descricao': 'Vaga para desenvolvedor backend com experiência em Python, Django e APIs REST. Atuará no desenvolvimento de sistemas corporativos.',
                'numVagas': 3, 
                'prazo': date.today() + timedelta(days=30),
                'instituicao': self.institutions['Tech Solutions'],
                'cursos': [self.courses['Ciência da Computação'], self.courses['Engenharia de Software']]
            },
            {
                'titulo': 'Estágio em Desenvolvimento Frontend', 
                'descricao': 'Vaga de estágio para desenvolvimento frontend com React, JavaScript e CSS. Ideal para estudantes de tecnologia.',
                'numVagas': 2, 
                'prazo': date.today() + timedelta(days=15),
                'instituicao': self.institutions['Inovação Digital'],
                'cursos': [self.courses['Ciência da Computação']]
            },
            {
                'titulo': 'Estágio em Administração', 
                'descricao': 'Vaga de estágio na área administrativa. Atividades incluem planilhas, relatórios e apoio à gestão.',
                'numVagas': 4, 
                'prazo': date.today() + timedelta(days=45),
                'instituicao': self.institutions['Banco Central'],
                'cursos': [self.courses['Administração']]
            },
        ]
        
        self.vagas = {}
        for vaga_data in vagas_data:
            vaga, created = Vaga.objects.get_or_create(
                titulo=vaga_data['titulo'],
                instituicao=vaga_data['instituicao'],
                defaults={
                    'descricao': vaga_data['descricao'],
                    'numVagas': vaga_data['numVagas'],
                    'prazo': vaga_data['prazo']
                }
            )
            self.vagas[vaga.titulo] = vaga

            if created:
                for curso in vaga_data['cursos']:
                    vaga.cursos.add(curso)
                self.stdout.write(self.style.SUCCESS(f"Vaga '{vaga.titulo}' criada com sucesso."))
            else:
                self.stdout.write(self.style.WARNING(f"Vaga '{vaga.titulo}' já existe."))
    
    def _setup_estagios(self):
        """Configura estágios de desenvolvimento"""
        self.stdout.write(self.style.SUCCESS("\n--- Criando Estágios de Desenvolvimento ---"))
        
        estagios_data = [
            {
                'aluno': self.users['aluno1'].perfil,
                'vaga': self.vagas['Desenvolvedor Backend Python'],
                'supervisor': self.users['supervisor1'].perfil,
                'orientador': self.users['orientador1'].perfil,
                'dt_ini': date.today() - timedelta(days=90),
                'dt_fim': date.today() + timedelta(days=90),
                'status': True,
                'nota': 8.5
            },
            {
                'aluno': self.users['aluno2'].perfil,
                'vaga': self.vagas['Estágio em Desenvolvimento Frontend'],
                'supervisor': self.users['supervisor1'].perfil,
                'orientador': None,
                'dt_ini': date.today() - timedelta(days=30),
                'dt_fim': date.today() + timedelta(days=150),
                'status': True,
                'nota': 9.0
            },
        ]
        
        for estagio_data in estagios_data:
            estagio, created = Estagio.objects.get_or_create(
                aluno=estagio_data['aluno'],
                vaga=estagio_data['vaga'],
                defaults=estagio_data
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f"Estágio criado: {estagio.aluno.user.username} na {estagio.vaga.titulo}"
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f"Estágio já existe: {estagio.aluno.user.username} na {estagio.vaga.titulo}"
                ))
    
