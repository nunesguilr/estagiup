from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .forms import InstituicaoForm
from .models import Instituicao
from usuario.models import Usuario
from django.db.models import Q
from vaga.models import Vaga


def instituicao_public(request):
    """
    View pública para listar e filtrar todas as instituições com status ativo.
    """
    instituicoes = Instituicao.objects.filter(status=True).order_by('nome')
    
    # Pega o termo de busca da URL (query GET)
    query = request.GET.get('q', '') # Usamos '' como padrão para evitar 'None'

    # Se o usuário digitou algo na busca, aplica o filtro
    if query:
        # A mágica do Q object: permite buscas complexas com 'OU' (|)
        instituicoes = instituicoes.filter(
            Q(nome__icontains=query) |
            Q(rua__icontains=query) |
            Q(bairro__icontains=query) |
            Q(cidade__icontains=query) |
            Q(estado__icontains=query) |
            Q(pais__icontains=query)
        )

    context = {
        'instituicoes': instituicoes,
        'search_query': query
    }
    return render(request, 'instituicao/instituicao_public.html', context)

def instituicao_public_detail(request, instituicao_id):
    instituicao = get_object_or_404(Instituicao, id=instituicao_id, status=True)
    
    # ACRESCENTADO: Busca todas as vagas relacionadas a esta instituição.
    # Futuramente, podemos adicionar um filtro de "status" aqui se o modelo Vaga tiver.
    vagas_da_instituicao = Vaga.objects.filter(instituicao=instituicao).order_by('-prazo')

    context = {
        'instituicao': instituicao,
        'vagas_da_instituicao': vagas_da_instituicao # ACRESCENTADO: Passa a lista de vagas para o template
    }
    return render(request, 'instituicao/instituicao_public_detail.html', context)

@login_required
@permission_required('instituicao.add_instituicao', raise_exception=True)
def cadastrar_instituicao(request):
    """
    View para o cadastro de uma nova instituição, onde o utilizador logado
    é automaticamente definido como o responsável.
    """
    try:
        # Acessa a instância de Usuario diretamente
        usuario = Usuario.objects.get(pk=request.user.pk)
    except Usuario.DoesNotExist:
        return redirect('dashboard')

    if request.method == 'POST':
        form = InstituicaoForm(request.POST)
        if form.is_valid():
            instituicao = form.save(commit=False)
            instituicao.save()

            instituicao.responsaveis.add(usuario)
            
            return redirect('instituicao:minhas_instituicoes')
        else:
            print("Erros no formulário:", form.errors)
    else:
        form = InstituicaoForm()

    context = {
        'form': form
    }
    return render(request, 'instituicao/cadastrar_instituicao.html', context)


@login_required
@permission_required('instituicao.change_instituicao', raise_exception=True)
def editar_instituicao(request, instituicao_id):
    """
    View para editar os dados de uma instituição.
    Apenas o responsável ou um admin podem editar.
    """
    instituicao = get_object_or_404(Instituicao, id=instituicao_id)
    
    # Acessa a instância de Usuario diretamente
    usuario = Usuario.objects.get(pk=request.user.pk)
    
    # Verifica a permissão de edição
    if usuario not in instituicao.responsaveis.all() and not request.user.is_superuser:
        return redirect('instituicao:minhas_instituicoes')
    
    if request.method == 'POST':
        form = InstituicaoForm(request.POST, instance=instituicao)
        if form.is_valid():
            instituicao_atualizada = form.save(commit=False)
            instituicao_atualizada.save()

            # Garante que a relação ManyToMany com o responsável seja mantida
            instituicao_atualizada.responsaveis.add(usuario)
            return redirect('instituicao:perfil_instituicao', instituicao_id=instituicao.id)
        else:
            print("Erros no formulário:", form.errors)
    else:
        form = InstituicaoForm(instance=instituicao)

    context = {
        'form': form,
        'instituicao': instituicao
    }
    return render(request, 'instituicao/editar_instituicao.html', context)

@login_required
@permission_required('instituicao.delete_instituicao', raise_exception=True)
def apagar_instituicao(request, instituicao_id):
    """
    View para apagar uma instituição.
    Apenas o responsável ou um admin podem apagar.
    """
    instituicao = get_object_or_404(Instituicao, id=instituicao_id)
    
    # Acessa a instância de Usuario diretamente
    usuario = Usuario.objects.get(pk=request.user.pk)
    
    # Verifica a permissão de exclusão
    if usuario not in instituicao.responsaveis.all() and not request.user.is_superuser:
        return redirect('instituicao:minhas_instituicoes')

    if request.method == 'POST':
        instituicao.delete()
        return redirect('instituicao:minhas_instituicoes')
    
    context = {
        'instituicao': instituicao
    }
    return render(request, 'instituicao/apagar_instituicao.html', context)

@login_required
def listar_membros_instituicao(request, instituicao_id):
    """
    View para listar os membros (responsáveis) de uma instituição específica.
    """
    instituicao = get_object_or_404(Instituicao, id=instituicao_id)
    membros = instituicao.responsaveis.all().select_related('user_ptr')
    
    try:
        # Acessa a instância de Usuario diretamente
        usuario = Usuario.objects.get(pk=request.user.pk)
        if usuario not in membros and not request.user.is_superuser:
            return redirect('dashboard')
    except Usuario.DoesNotExist:
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
        # Acessa a instância de Usuario diretamente
        usuario = Usuario.objects.get(pk=request.user.pk)
        minhas_instituicoes = Instituicao.objects.filter(responsaveis=usuario)
    except Usuario.DoesNotExist:
        minhas_instituicoes = Instituicao.objects.none()
    
    context = {
        'minhas_instituicoes': minhas_instituicoes
    }
    return render(request, 'instituicao/minhas_instituicoes.html', context)

def perfil_instituicao(request, instituicao_id):
    """
    View para exibir o perfil de uma instituição específica.
    """
    instituicao = get_object_or_404(Instituicao, id=instituicao_id)
    responsaveis = instituicao.responsaveis.all().select_related('user_ptr')
    
    context = {
        'instituicao': instituicao,
        'responsaveis': responsaveis
    }
    return render(request, 'instituicao/perfil_instituicao.html', context)
