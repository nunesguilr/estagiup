# vaga/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from .models import Vaga
from .forms import VagaForm

@login_required
def vaga_list(request):
    """
    Lista todas as vagas disponíveis.
    """
    vagas = Vaga.objects.all().select_related('instituicao').order_by('-prazo')
    
    # Filtro por busca
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
    
    # Verifica se o usuário pode editar/apagar a vaga
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
def vaga_create(request):
    """
    View para o cadastro de uma nova vaga.
    """
    if request.method == 'POST':
        form = VagaForm(request.POST, user=request.user)
        if form.is_valid():
            vaga = form.save(commit=False)
            
            # Se o usuário tem perfil e está associado a uma instituição
            if hasattr(request.user, 'perfil') and request.user.perfil.instituicao:
                vaga.instituicao = request.user.perfil.instituicao
            
            vaga.save()
            form.save_m2m()  # Salva a relação ManyToMany com os cursos
            messages.success(request, 'Vaga cadastrada com sucesso!')
            return redirect('vaga:vaga_detail', vaga_id=vaga.id)
        else:
            messages.error(request, 'Erro ao cadastrar a vaga. Por favor, verifique os campos.')
    else:
        form = VagaForm(user=request.user)

    context = {
        'form': form,
        'title': 'Cadastrar Nova Vaga'
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
    
    # Verifica a permissão de edição
    can_edit = False
    if hasattr(request.user, 'perfil') and vaga.instituicao:
        can_edit = (request.user.perfil in vaga.instituicao.responsaveis.all() or 
                   request.user.is_superuser)
    
    if not can_edit:
        messages.error(request, 'Você não tem permissão para editar esta vaga.')
        return redirect('vaga:vaga_detail', vaga_id=vaga.id)
    
    if request.method == 'POST':
        form = VagaForm(request.POST, instance=vaga, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Vaga "{vaga.titulo}" atualizada com sucesso!')
            return redirect('vaga:vaga_detail', vaga_id=vaga.id)
        else:
            messages.error(request, 'Erro ao atualizar a vaga. Por favor, verifique os campos.')
    else:
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
    
    # Verifica a permissão de exclusão
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
    vagas = Vaga.objects.filter(ativa=True).select_related('instituicao').order_by('-prazo')
    
    # Filtro por busca
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