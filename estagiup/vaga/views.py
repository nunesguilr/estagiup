from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from .models import Vaga
from .forms import VagaForm
from instituicao.models import Instituicao
from usuario.models import Usuario

@login_required
def vaga_list(request):
    """
    Lista todas as vagas disponíveis para gerenciamento interno.
    """
    if not request.user.is_superuser and not request.user.groups.filter(name='Responsaveis da Instituicao').exists():
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
