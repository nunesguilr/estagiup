from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import InstituicaoForm
from .models import Instituicao
from usuario.models import PerfilUsuario  # Importa o modelo PerfilUsuario

@login_required
def cadastrar_instituicao(request):
    """
    View para o cadastro de uma nova instituição, onde o utilizador logado
    é automaticamente definido como o responsável.
    """
    try:
        # Tenta obter o perfil do utilizador logado
        perfil_usuario = request.user.perfil
    except PerfilUsuario.DoesNotExist:
        # Se o perfil não existir, exibe um erro e impede o cadastro
        messages.error(request, 'O seu utilizador não tem um perfil associado. Por favor, complete o seu perfil antes de cadastrar uma instituição.')
        return redirect('dashboard') # Redireciona para um local seguro.

    if request.method == 'POST':
        form = InstituicaoForm(request.POST)
        if form.is_valid():
            instituicao = form.save(commit=False)
            instituicao.save()

            # Adiciona o utilizador logado como responsável pela instituição.
            instituicao.responsaveis.add(perfil_usuario)
            
            messages.success(request, 'Instituição cadastrada com sucesso! Você foi definido como o responsável.')
            return redirect('instituicao:cadastrar')
        else:
            messages.error(request, 'Erro ao cadastrar a instituição. Por favor, verifique os campos.')
    else:
        form = InstituicaoForm()

    context = {
        'form': form
    }
    return render(request, 'instituicao/cadastrar_instituicao.html', context)


@login_required
def listar_membros_instituicao(request, instituicao_id):
    """
    View para listar os membros (responsáveis) de uma instituição específica.
    """
    instituicao = get_object_or_404(Instituicao, id=instituicao_id)
    membros = instituicao.responsaveis.all().select_related('user')
    
    if request.user.perfil not in membros and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para aceder a esta página.')
        return redirect('dashboard')
    
    context = {
        'instituicao': instituicao,
        'membros': membros,
    }
    return render(request, 'instituicao/membros.html', context)

def perfil_instituicao(request, instituicao_id):
    """
    View para exibir o perfil de uma instituição específica.
    """
    instituicao = get_object_or_404(Instituicao, id=instituicao_id)

    # Busca os responsáveis da instituição para exibir no template
    responsaveis = instituicao.responsaveis.all().select_related('user')

    context = {
        'instituicao': instituicao,
        'responsaveis': responsaveis
    }
    return render(request, 'instituicao/perfil.html', context)
