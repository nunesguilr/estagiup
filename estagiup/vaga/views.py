# vaga/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import Vaga
from .forms import VagaForm
from usuario.models import PerfilUsuario

@login_required
def vaga_list(request):
    """
    Lista todas as vagas disponíveis.
    """
    vagas = Vaga.objects.all().select_related('instituicao').order_by('-prazo')
    context = {
        'vagas': vagas
    }
    return render(request, 'vaga/vaga_list.html', context)


@login_required
def vaga_detail(request, vaga_id):
    """
    Exibe os detalhes de uma vaga específica.
    """
    vaga = get_object_or_404(Vaga, id=vaga_id)
    context = {
        'vaga': vaga
    }
    return render(request, 'vaga/vaga_detail.html', context)


@login_required
@permission_required('vaga.add_vaga', raise_exception=True)
def vaga_create(request):
    """
    View para o cadastro de uma nova vaga.
    """
    if request.method == 'POST':
        form = VagaForm(request.POST)
        if form.is_valid():
            vaga = form.save(commit=False)
            # Associa a vaga à instituição do responsável
            vaga.save()
            form.save_m2m() # Salva a relação ManyToMany com os cursos
            messages.success(request, 'Vaga cadastrada com sucesso!')
            return redirect('vaga:vaga_list')
        else:
            messages.error(request, 'Erro ao cadastrar a vaga. Por favor, verifique os campos.')
    else:
        form = VagaForm()

    context = {
        'form': form
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
    if request.user.perfil not in vaga.instituicao.responsaveis.all() and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para editar esta vaga.')
        return redirect('vaga:vaga_detail', vaga_id=vaga.id)
    
    if request.method == 'POST':
        form = VagaForm(request.POST, instance=vaga)
        if form.is_valid():
            form.save()
            messages.success(request, f'Vaga "{vaga.titulo}" atualizada com sucesso!')
            return redirect('vaga:vaga_detail', vaga_id=vaga.id)
        else:
            messages.error(request, 'Erro ao atualizar a vaga. Por favor, verifique os campos.')
    else:
        form = VagaForm(instance=vaga)

    context = {
        'form': form,
        'vaga': vaga
    }
    return render(request, 'vaga/vaga_form.html', context)


@login_required
@permission_required('vaga.delete_vaga', raise_exception=True)
def vaga_delete(request, vaga_id):
    """
    Permite apagar uma vaga.
    """
    vaga = get_object_or_404(Vaga, id=vaga_id)
    
    if request.user.perfil not in vaga.instituicao.responsaveis.all() and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para apagar esta vaga.')
        return redirect('vaga:vaga_detail', vaga_id=vaga.id)

    if request.method == 'POST':
        vaga.delete()
        messages.success(request, f'Vaga "{vaga.titulo}" apagada com sucesso.')
        return redirect('vaga:vaga_list')
        
    context = {
        'vaga': vaga
    }
    return render(request, 'vaga/vaga_confirm_delete.html', context)
