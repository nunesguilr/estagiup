from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from .models import Vaga
from .forms import VagaForm
from instituicao.models import Instituicao
from usuario.models import Usuario
from estagio.models import Estagio
from curso.models import Curso 

@login_required
def vaga_list(request):
    """
    Lista as vagas relevantes para o usuário logado no dashboard.
    - Superusuários e Responsáveis veem todas as vagas que podem gerenciar.
    - Alunos veem todas as vagas para as quais podem se candidatar.
    - Outros perfis (Orientador, Supervisor) não têm uma lista de "gerenciamento de vagas".
    """
    user = request.user
    
    # Se o usuário não tem um grupo, redireciona para o dashboard.
    if not user.groups.exists() and not user.is_superuser:
        messages.warning(request, "Seu usuário não está associado a um perfil.")
        return redirect('dashboard')

    user_group = user.groups.first().name if user.groups.exists() else None

    if user.is_superuser or user_group == 'Responsaveis da Instituicao':
        # Para Admins e Responsáveis, mostra todas as vagas para gerenciamento
        vagas = Vaga.objects.all().select_related('instituicao').order_by('-prazo')
        
        # Um responsável vê apenas as vagas das suas instituições
        if user_group == 'Responsaveis da Instituicao':
            vagas = vagas.filter(instituicao__responsaveis=user)

    elif user_group == 'Alunos':
        # Alunos veem todas as vagas, similar à visão pública, mas no dashboard
        vagas = Vaga.objects.all().select_related('instituicao').order_by('-prazo')

    else:
        # Orientadores e Supervisores não têm acesso a esta página de gerenciamento
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('dashboard')

    context = {
        'vagas': vagas,
    }
    return render(request, 'vaga/vaga_list.html', context)

@login_required
def vaga_detail(request, vaga_id):
    """
    Exibe os detalhes de uma vaga específica.
    """
    vaga = get_object_or_404(Vaga, id=vaga_id)
    
    if not request.user.is_superuser and not request.user.groups.filter(name='Alunos').exists():
        return redirect('vaga:vaga_list')
        
    can_edit = False
    if vaga.instituicao:
        can_edit = (request.user in vaga.instituicao.responsaveis.all() or 
                    request.user.is_superuser)
    
    context = {
        'vaga': vaga,
        'can_edit': can_edit
    }
    return render(request, 'vaga/vaga_detail.html', context)

@login_required
def selecionar_instituicao_para_vaga(request):
    """
    Página intermediária para o usuário selecionar a qual de suas
    instituições ele deseja adicionar uma nova vaga.
    """
    try:
        # Busca todas as instituições pelas quais o usuário é responsável
        instituicoes_do_usuario = Instituicao.objects.filter(responsaveis=request.user)
    except Usuario.DoesNotExist: # Ajuste para PerfilUsuario.DoesNotExist se necessário
        instituicoes_do_usuario = []

    if not instituicoes_do_usuario.exists():
        messages.warning(request, 'Você precisa ser responsável por pelo menos uma instituição para adicionar uma vaga.')
        return redirect('instituicao:minhas_instituicoes')

    context = {
        'instituicoes': instituicoes_do_usuario,
        'title': 'Selecionar Instituição'
    }
    return render(request, 'vaga/select_instituicao.html', context)

@login_required
@permission_required('vaga.add_vaga', raise_exception=True)
def vaga_create(request, instituicao_id):
    """
    View para o cadastro de uma nova vaga para uma instituição específica.
    """
    instituicao = get_object_or_404(Instituicao, pk=instituicao_id)

    if not request.user.is_superuser and request.user not in instituicao.responsaveis.all():
        return redirect('instituicao:minhas_instituicoes')

    if request.method == 'POST':
        # Instanciar o formulário, passando a instância do utilizador para que ele possa ser validado
        form = VagaForm(request.POST, user=request.user)
        if form.is_valid():
            vaga = form.save(commit=False)
            vaga.instituicao = instituicao
            vaga.save()
            form.save_m2m() # Salva a relação ManyToMany
            return redirect('vaga:vaga_detail', vaga_id=vaga.id)
        else:
            # Re-renderiza o formulário com erros de validação
            pass
    else:
        # Instanciar o formulário, passando a instância do utilizador para que ele possa ser validado
        form = VagaForm(user=request.user)

    context = {
        'form': form,
        'instituicao': instituicao,
        'title': f'Cadastrar Nova Vaga para {instituicao.nome}'
    }
    return render(request, 'vaga/vaga_form.html', context)

@login_required
@permission_required('vaga.change_vaga', raise_exception=True)
def vaga_update(request, vaga_id):
    """
    Permite editar os dados de uma vaga.
    Apenas o responsável da instituição que a criou pode editar.
    """
    vaga = get_object_or_404(Vaga, id=vaga_id)
    
    can_edit = False
    if vaga.instituicao:
        can_edit = (request.user in vaga.instituicao.responsaveis.all() or 
                    request.user.is_superuser)
    
    if not can_edit:
        return redirect('vaga:vaga_detail', vaga_id=vaga.id)
    
    if request.method == 'POST':
        # Instanciar o formulário com a instância da vaga e do utilizador
        form = VagaForm(request.POST, instance=vaga, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('vaga:vaga_detail', vaga_id=vaga.id)
        else:
            # Re-renderiza o formulário com erros de validação
            pass
    else:
        # Instanciar o formulário com a instância da vaga e do utilizador
        form = VagaForm(instance=vaga, user=request.user)

    context = {
        'form': form,
        'vaga': vaga,
        'title': f'Editar Vaga: {vaga.titulo}'
    }
    return render(request, 'vaga/vaga_form.html', context)

@login_required
@permission_required('vaga.delete_vaga', raise_exception=True)
def vaga_delete(request, vaga_id):
    """
    Permite apagar uma vaga.
    """
    vaga = get_object_or_404(Vaga, id=vaga_id)
    
    can_delete = False
    if vaga.instituicao:
        can_delete = (request.user in vaga.instituicao.responsaveis.all() or 
                      request.user.is_superuser)
    
    if not can_delete:
        return redirect('vaga:vaga_detail', vaga_id=vaga.id)

    if request.method == 'POST':
        vaga.delete()
        return redirect('vaga:vaga_list')
        
    context = {
        'vaga': vaga
    }
    return render(request, 'vaga/vaga_confirm_delete.html', context)

def vaga_public(request):
    """
    View pública para listar e filtrar vagas.
    """
    vagas = Vaga.objects.select_related('instituicao').order_by('-prazo')
    
    # Busca todas as instituições e cursos para popular os filtros
    instituicoes = Instituicao.objects.filter(status=True).order_by('nome')
    cursos = Curso.objects.all().order_by('nome')

    # Pega os valores dos filtros da URL (query GET)
    query = request.GET.get('q', '')
    instituicao_id = request.GET.get('instituicao', '')
    curso_id = request.GET.get('curso', '')

    # Aplica o filtro de busca por texto, se houver
    if query:
        vagas = vagas.filter(
            Q(titulo__icontains=query) |
            Q(descricao__icontains=query)
        )
    
    # Aplica o filtro por instituição, se houver
    if instituicao_id:
        vagas = vagas.filter(instituicao_id=instituicao_id)

    # Aplica o filtro por curso, se houver
    if curso_id:
        vagas = vagas.filter(cursos__id=curso_id)
    
    context = {
        'vagas': vagas,
        'instituicoes': instituicoes,
        'cursos': cursos,
        'search_query': query,
        'selected_instituicao': int(instituicao_id) if instituicao_id else None,
        'selected_curso': int(curso_id) if curso_id else None,
    }
    return render(request, 'vaga/vaga_public.html', context)

def vaga_public_detail(request, vaga_id):
    """
    Exibe os detalhes públicos de uma vaga específica.
    """
    vaga = get_object_or_404(Vaga, id=vaga_id)
    
    # Lógica para o botão de candidatura
    ja_se_candidatou = False
    is_aluno = False
    
    if request.user.is_authenticated and hasattr(request.user, 'perfil'):
        if request.user.groups.filter(name='Alunos').exists():
            is_aluno = True
            # Verifica se já existe um estágio para este aluno e esta vaga
            ja_se_candidatou = Estagio.objects.filter(vaga=vaga, aluno=request.user).exists()

    context = {
        'vaga': vaga,
        'ja_se_candidatou': ja_se_candidatou,
        'is_aluno': is_aluno,
    }
    return render(request, 'vaga/vaga_public_detail.html', context)