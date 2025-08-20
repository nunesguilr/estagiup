from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import InstituicaoForm
from .models import Instituicao
from usuario.models import PerfilUsuario

@login_required
def cadastrar_instituicao(request):
    """
    View para o cadastro de uma nova instituição, onde o utilizador logado
    é automaticamente definido como o responsável.
    """
    try:
        perfil_usuario = request.user.perfil
    except PerfilUsuario.DoesNotExist:
        messages.error(request, 'O seu utilizador não tem um perfil associado. Por favor, complete o seu perfil antes de cadastrar uma instituição.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = InstituicaoForm(request.POST)
        if form.is_valid():
            instituicao = form.save(commit=False)
            instituicao.save()

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
    
    try:
        if request.user.perfil not in membros and not request.user.is_superuser:
            messages.error(request, 'Você não tem permissão para aceder a esta página.')
            return redirect('dashboard')
    except PerfilUsuario.DoesNotExist:
        messages.error(request, 'O seu utilizador não tem um perfil associado.')
        return redirect('dashboard')
    
    context = {
        'instituicao': instituicao,
        'membros': membros,
    }
    return render(request, 'instituicao/membros.html', context)


@login_required
def minhas_instituicoes(request):
    """
    View para listar todas as instituições para as quais o utilizador logado é responsável.
    """
    try:
        perfil_usuario = request.user.perfil
        minhas_instituicoes = Instituicao.objects.filter(responsaveis=perfil_usuario)
    except PerfilUsuario.DoesNotExist:
        minhas_instituicoes = []
    
    context = {
        'minhas_instituicoes': minhas_instituicoes
    }
    return render(request, 'instituicao/minhas_instituicoes.html', context)

def perfil_instituicao(request, instituicao_id):
    """
    View para exibir o perfil de uma instituição específica.
    """
    instituicao = get_object_or_404(Instituicao, id=instituicao_id)
    responsaveis = instituicao.responsaveis.all().select_related('user')
    
    context = {
        'instituicao': instituicao,
        'responsaveis': responsaveis
    }
    return render(request, 'instituicao/perfil_instituicao.html', context)
