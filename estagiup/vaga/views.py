# vaga/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from .models import Vaga
from .forms import VagaForm
from instituicao.models import Instituicao
from usuario.models import PerfilUsuario

@login_required
def vaga_list(request):
    """
    Lista todas as vagas disponíveis para gerenciamento interno.
    """
    if not request.user.is_superuser and not request.user.groups.filter(name='Responsaveis da Instituicao').exists():
        messages.error(request, 'Você não tem permissão para gerenciar vagas.')
        return redirect('dashboard')
    
    vagas = Vaga.objects.all().select_related('instituicao').order_by('-prazo')
    
    query = request.GET.get('q')
    if query:
        vagas = vagas.filter(
            Q(titulo__icontains=query) |
            Q(descricao__icontains=query) |
            Q(instituicao__nome__icontains=query)
        )
    
    context = {
        'vagas': vagas,
        'search_query': query
    }
    return render(request, 'vaga/vaga_list.html', context)

@login_required
def vaga_detail(request, vaga_id):
    """
    Exibe os detalhes de uma vaga específica.
    """
    vaga = get_object_or_404(Vaga, id=vaga_id)
    
    if not request.user.is_superuser and not request.user.groups.filter(name='Alunos').exists():
        messages.error(request, 'Você não tem permissão para visualizar esta vaga.')
        return redirect('vaga:vaga_list')
        
    can_edit = False
    if hasattr(request.user, 'perfil') and vaga.instituicao:
        can_edit = (request.user.perfil in vaga.instituicao.responsaveis.all() or 
                    request.user.is_superuser)
    
    context = {
        'vaga': vaga,
        'can_edit': can_edit
    }
    return render(request, 'vaga/vaga_detail.html', context)

@login_required
@permission_required('vaga.add_vaga', raise_exception=True)
def vaga_create(request, instituicao_id):
    """
    View para o cadastro de uma nova vaga para uma instituição específica.
    """
    instituicao = get_object_or_404(Instituicao, pk=instituicao_id)

    if not request.user.is_superuser and request.user.perfil not in instituicao.responsaveis.all():
        messages.error(request, "Você não tem permissão para adicionar vagas nesta instituição.")
        return redirect('instituicao:minhas_instituicoes')

    if request.method == 'POST':
        # Correção: Agora passamos 'user=request.user' para o formulário.
        form = VagaForm(request.POST, user=request.user)
        if form.is_valid():
            vaga = form.save(commit=False)
            vaga.instituicao = instituicao
            vaga.save()
            form.save_m2m()
            messages.success(request, 'Vaga cadastrada com sucesso!')
            return redirect('vaga:vaga_detail', vaga_id=vaga.id)
        else:
            messages.error(request, 'Erro ao cadastrar a vaga. Por favor, verifique os campos.')
    else:
        # Correção: Agora passamos 'user=request.user' para o formulário.
        form = VagaForm(user=request.user)

    context = {
        'form': form,
        'instituicao': instituicao,
        'title': f'Cadastrar Nova Vaga para {instituicao.nome}'
    }
    return render(request, 'vaga/vaga_form.html', context)

@login_required
def selecionar_instituicao_para_vaga(request):
    """
    Página intermediária para o usuário selecionar a qual de suas
    instituições ele deseja adicionar uma nova vaga.
    """
    try:
        instituicoes_do_usuario = Instituicao.objects.filter(responsaveis=request.user.perfil)
    except PerfilUsuario.DoesNotExist:
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
@permission_required('vaga.change_vaga', raise_exception=True)
def vaga_update(request, vaga_id):
    """
    Permite editar os dados de uma vaga.
    Apenas o responsável da instituição que a criou pode editar.
    """
    vaga = get_object_or_404(Vaga, id=vaga_id)
    
    can_edit = False
    if hasattr(request.user, 'perfil') and vaga.instituicao:
        can_edit = (request.user.perfil in vaga.instituicao.responsaveis.all() or 
                    request.user.is_superuser)
    
    if not can_edit:
        messages.error(request, 'Você não tem permissão para editar esta vaga.')
        return redirect('vaga:vaga_detail', vaga_id=vaga.id)
    
    if request.method == 'POST':
        # Correção: Já estava correto, mas mantive a explicitação para consistência.
        form = VagaForm(request.POST, instance=vaga, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Vaga "{vaga.titulo}" atualizada com sucesso!')
            return redirect('vaga:vaga_detail', vaga_id=vaga.id)
        else:
            messages.error(request, 'Erro ao atualizar a vaga. Por favor, verifique os campos.')
    else:
        # Correção: Já estava correto, mas mantive a explicitação para consistência.
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
    if hasattr(request.user, 'perfil') and vaga.instituicao:
        can_delete = (request.user.perfil in vaga.instituicao.responsaveis.all() or 
                      request.user.is_superuser)
    
    if not can_delete:
        messages.error(request, 'Você não tem permissão para apagar esta vaga.')
        return redirect('vaga:vaga_detail', vaga_id=vaga.id)

    if request.method == 'POST':
        titulo = vaga.titulo
        vaga.delete()
        messages.success(request, f'Vaga "{titulo}" apagada com sucesso.')
        return redirect('vaga:vaga_list')
        
    context = {
        'vaga': vaga
    }
    return render(request, 'vaga/vaga_confirm_delete.html', context)

def vaga_public(request):
    """
    View pública para listar vagas (sem requerer login)
    """
    vagas = Vaga.objects.all().select_related('instituicao').order_by('-prazo')
    
    query = request.GET.get('q')
    if query:
        vagas = vagas.filter(
            Q(titulo__icontains=query) |
            Q(descricao__icontains=query) |
            Q(instituicao__nome__icontains=query)
        )
    
    context = {
        'vagas': vagas,
        'search_query': query,
        'public_view': True
    }
    return render(request, 'vaga/vaga_public.html', context)

def vaga_public_detail(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    context = {
        'vaga': vaga
    }
    return render(request, 'vaga/vaga_public_detail.html', context)
