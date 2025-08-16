# usuario/management/commands/create_permissions.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError

# Importa todos os modelos do projeto para atribuir permissões.
# Certifique-se de que estes modelos estão corretamente importados.
from usuario.models import PerfilUsuario
from instituicao.models import Instituicao
from vaga.models import Vaga
from curso.models import Curso
from estagio.models import Estagio

class Command(BaseCommand):
    help = 'Cria os grupos de usuários padrão e atribui as permissões definidas.'

    def handle(self, *args, **options):
        # 1. Criação dos Grupos.
        # Use um dicionário para definir os grupos e as permissões associadas.
        groups_permissions_map = {
            'Alunos': [
                ('view_perfilusuario', PerfilUsuario),
                ('change_perfilusuario', PerfilUsuario), # Lógica de permissão por objeto deve ser implementada na view.
                ('view_vaga', Vaga),
                ('view_curso', Curso),
                ('view_estagio', Estagio),
                ('add_estagio', Estagio),
            ],
            'Responsaveis da Instituicao': [
                ('view_instituicao', Instituicao),
                ('change_instituicao', Instituicao),
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
            ],
            'Orientadores': [
                ('view_estagio', Estagio),
                ('view_perfilusuario', PerfilUsuario),
            ],
        }

        # Função auxiliar para obter permissões de forma segura.
        def get_permission(codename, model):
            try:
                content_type = ContentType.objects.get_for_model(model)
                return Permission.objects.get(codename=codename, content_type=content_type)
            except (ContentType.DoesNotExist, Permission.DoesNotExist):
                return None

        self.stdout.write(self.style.SUCCESS("Iniciando a criação de grupos e atribuição de permissões..."))

        for group_name, permissions_list in groups_permissions_map.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Grupo '{group.name}' criado com sucesso."))
            else:
                self.stdout.write(self.style.WARNING(f"Grupo '{group.name}' já existe."))
            
            # Adiciona as permissões ao grupo.
            for codename, model in permissions_list:
                perm = get_permission(codename, model)
                if perm:
                    try:
                        group.permissions.add(perm)
                        self.stdout.write(self.style.SUCCESS(f"  - Permissão '{perm.codename}' adicionada ao grupo '{group.name}'."))
                    except IntegrityError:
                        self.stdout.write(self.style.WARNING(f"  - Permissão '{perm.codename}' já existe no grupo '{group.name}'."))
                else:
                    self.stdout.write(self.style.ERROR(f"  - Permissão '{codename}' para o modelo '{model.__name__}' não encontrada. Verifique se as migrações foram executadas."))

        self.stdout.write(self.style.SUCCESS("\nProcesso de atribuição de permissões concluído."))
        self.stdout.write(self.style.WARNING("Lembre-se: As permissões de Admin (is_superuser) são concedidas diretamente ao utilizador, não a um grupo."))
