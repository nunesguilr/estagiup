from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Usuario, Aluno, ContaEmpresa, Supervisor, Professor, ContaInstituicao

# Registra os modelos de perfil no admin
admin.site.register(Aluno)
admin.site.register(ContaEmpresa)
admin.site.register(Supervisor)
admin.site.register(Professor)
admin.site.register(ContaInstituicao)

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'tipo_usuario', 'data_cadastro', 'get_related_profile_type')
    search_fields = ('nome', 'email', 'tipo_usuario')
    list_filter = ('tipo_usuario',)

    def get_related_profile_type(self, obj):
        # Esta função auxiliar verifica se o usuário tem um perfil associado
        # e retorna o tipo, se houver.
        # É útil para visualização no list_display
        if hasattr(obj, 'aluno') and obj.aluno:
            return 'Aluno'
        if hasattr(obj, 'contaempresa') and obj.contaempresa:
            return 'Empresa'
        if hasattr(obj, 'professor') and obj.professor:
            return 'Professor'
        if hasattr(obj, 'supervisor') and obj.supervisor:
            return 'Supervisor'
        if hasattr(obj, 'instituicao') and obj.instituicao:
            return 'Instituição'
        return 'Nenhum'
    get_related_profile_type.short_description = 'Tipo de Perfil Associado'

    def save_model(self, request, obj, form, change):
        # Este método é chamado antes de salvar o objeto Usuario no Admin

        # Se o usuário já existe e está sendo editado (não é um novo usuário sendo criado do zero)
        if obj.pk:
            # Obtém o estado atual do usuário antes das mudanças do formulário
            original_obj = Usuario.objects.get(pk=obj.pk)
            original_profile_type = self.get_related_profile_type(original_obj)
        else:
            original_profile_type = 'Nenhum' # Novo usuário não tem perfil associado inicialmente

        # Percorre todos os tipos de perfil e verifica se o usuário já possui um
        # diferente do que está sendo potencialmente associado agora.
        # Esta lógica assume que você criará o perfil específico (Aluno, Empresa, etc.)
        # EM SEPARADO depois de criar o Usuario.
        # Se você estiver criando o perfil E o Usuario no mesmo formulário admin,
        # a lógica precisaria ser um pouco diferente.
        
        # O problema é mais comum quando se tenta criar um NOVO PERFIL
        # para um USUARIO JÁ EXISTENTE que já tem OUTRO TIPO de perfil.
        
        # Esta validação é mais eficaz se aplicada na criação dos perfis (AlunoAdmin, EmpresaAdmin, etc.)
        # Ou se o UsuarioAdmin é o PONTO CENTRAL para criar QUALQUER TIPO de perfil.

        # PARA APLICAR A VALIDAÇÃO:
        # A forma mais robusta de garantir "um usuário só um tipo de perfil"
        # quando a criação de perfis é feita em telas separadas (Admin, ou views customizadas)
        # é validar na criação/edição do *perfil específico* (Aluno, Empresa, etc.).
        # O UsuarioAdmin sozinho não consegue impedir que um Admin crie um Aluno, depois vá
        # e crie uma ContaEmpresa para o MESMO Usuario.
        # Ele só pode tentar impedir se o "tipo_usuario" do Usuario estiver sendo mudado
        # e já houver outro perfil.

        # Exemplo de validação no save_model do UsuarioAdmin (mais útil se o tipo_usuario for alterado aqui)
        # if change and original_profile_type != 'Nenhum' and original_profile_type != obj.tipo_usuario.capitalize():
        #     raise ValidationError(f"Este usuário já está associado a um perfil do tipo '{original_profile_type}'. Não é possível alterar o tipo de usuário ou associar outro tipo de perfil.")
        
        # A validação mais eficaz deve ser feita nos admin-forms dos perfis ALUNO, EMPRESA, etc.
        # Isso será adicionado abaixo.

        super().save_model(request, obj, form, change)

# Registra o modelo Usuario com o admin customizado
admin.site.register(Usuario, UsuarioAdmin)


# --- Validação Adicional nos ModelAdmin dos Perfis Específicos ---
# Esta é a parte CRÍTICA para garantir que um USUARIO só tenha UM TIPO DE PERFIL.
# Quando você tenta criar um Aluno (ou Empresa, etc.) para um Usuário,
# este Admin irá verificar se esse Usuário já tem QUALQUER outro tipo de perfil.

# Desregistra os modelos para poder registrar com classes customizadas
admin.site.unregister(Aluno)
admin.site.unregister(ContaEmpresa)
admin.site.unregister(Supervisor)
admin.site.unregister(Professor)
admin.site.unregister(ContaInstituicao)


class BaseProfileAdmin(admin.ModelAdmin):
    # Uma classe base para reutilizar a lógica de validação
    def clean(self):
        cleaned_data = super().clean()
        usuario = cleaned_data.get('usuario')
        if not usuario:
            # Se o usuário não foi selecionado, deixe a validação padrão de campo obrigatório.
            return cleaned_data

        # Lista de todos os modelos de perfil que um usuário pode ter
        profile_models = {
            'aluno': Aluno,
            'empresa': ContaEmpresa,
            'professor': Professor,
            'supervisor': Supervisor,
            'instituicao': ContaInstituicao
        }

        # Itera sobre os tipos de perfil para verificar se o usuário já tem um
        # Ignora o tipo de perfil que está sendo salvo atualmente
        for profile_type, model_class in profile_models.items():
            if model_class._meta.model_name != self.model._meta.model_name and hasattr(usuario, model_class._meta.model_name):
                # Se o usuário já tem um perfil de OUTRO TIPO
                # E esse perfil não é nulo (realmente existe)
                if getattr(usuario, model_class._meta.model_name, None) is not None:
                    # Permite se estiver editando o PRÓPRIO perfil existente e não criando um novo
                    if self.instance and self.instance.pk: # Se é uma edição
                        if getattr(usuario, model_class._meta.model_name).pk == self.instance.pk:
                            continue # Permitido se estiver editando o próprio perfil
                    
                    raise ValidationError(
                        f"Este usuário ('{usuario.nome}' - {usuario.email}) já está associado a um perfil do tipo '{model_class._meta.verbose_name.capitalize()}'. Um usuário só pode ter um tipo de perfil associado."
                    )
        return cleaned_data

class AlunoAdmin(BaseProfileAdmin):
    # list_display, search_fields, etc. podem ser adicionados aqui
    pass # Exemplo: list_display = ('usuario', 'matricula', 'curso')

class ContaEmpresaAdmin(BaseProfileAdmin):
    pass

class SupervisorAdmin(BaseProfileAdmin):
    pass

class ProfessorAdmin(BaseProfileAdmin):
    pass

class ContaInstituicaoAdmin(BaseProfileAdmin):
    pass


# Registra os modelos de perfil com as classes de Admin customizadas
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(ContaEmpresa, ContaEmpresaAdmin)
admin.site.register(Supervisor, SupervisorAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(ContaInstituicao, ContaInstituicaoAdmin)

