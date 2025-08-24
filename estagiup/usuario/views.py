# Em usuario/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

# Importando NOSSOS formulários customizados e os do Guilherme
from .forms import UserRegistrationForm, UserAuthenticationForm, PerfilUpdateForm
from .models import PerfilUsuario

def registrar_usuario(request):
    """
    View para registar um novo utilizador, seu perfil e atribuí-lo a um grupo.
    (Versão do Guilherme, está ótima)
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Bem-vindo(a), {user.username}! O seu registo foi concluído com sucesso.')
            return redirect('usuario:login') # Corrigido para usar o namespace
        else:
            messages.error(request, 'Houve um erro no seu registo. Por favor, verifique os campos em destaque.')
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'usuario/registrar_usuario.html', context)


def login_usuario(request):
    """
    View para a página de login.
    (MANTIVEMOS A NOSSA VERSÃO para usar o formulário customizado e estiloso)
    """
    if request.method == 'POST':
        form = UserAuthenticationForm(request, data=request.POST) # <-- Usando nosso form
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # messages.success(request, f'Bem-vindo(a) de volta, {user.username}!')
            return redirect('dashboard') # Redireciona para o dashboard principal
    else:
        form = UserAuthenticationForm() # <-- Usando nosso form

    context = {
        'form': form
    }
    return render(request, 'usuario/login.html', context)


def lista_usuarios(request):
    """
    View para exibir uma lista de todos os utilizadores e seus perfis.
    (MANTIVEMOS A NOSSA VERSÃO para enviar a lista de grupos para o filtro)
    """
    todos_usuarios = PerfilUsuario.objects.all().select_related('user').order_by('user__username')
    todos_grupos = Group.objects.all() # <-- A linha que faz o filtro dinâmico funcionar

    context = {
        'todos_usuarios': todos_usuarios,
        'todos_grupos': todos_grupos # <-- Enviando os grupos para o template
    }
    return render(request, 'usuario/lista.html', context)


@login_required # <-- Adicionado o decorador de login
def user_detail(request, pk): # <-- Nome da view e parâmetro atualizados
    """
    View para exibir os detalhes de um utilizador específico.
    (Usando a versão otimizada do Guilherme)
    """
    target_user = get_object_or_404(User, pk=pk)
    context = {
        'target_user': target_user
    }
    return render(request, 'usuario/user_detail.html', context)


# MANTENDO AS NOVAS VIEWS DO GUILHERME
@login_required
def editar_perfil(request):
    """
    View para que o utilizador logado edite o seu próprio perfil.
    """
    try:
        perfil = request.user.perfil
    except PerfilUsuario.DoesNotExist:
        # Criar um perfil se não existir
        perfil = PerfilUsuario.objects.create(user=request.user)
        messages.info(request, 'Um perfil foi criado para você.')

    if request.method == 'POST':
        form = PerfilUpdateForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'O seu perfil foi atualizado com sucesso!')
            return redirect('usuario:editar_perfil')
        else:
            messages.error(request, 'Erro ao atualizar o perfil. Por favor, verifique os campos.')
    else:
        form = PerfilUpdateForm(instance=perfil)

    context = {
        'form': form
    }
    return render(request, 'usuario/editar_perfil.html', context)


@login_required
def apagar_usuario(request):
    """
    View para apagar o utilizador logado.
    """
    if request.method == 'POST':
        # Apagamos o utilizador logado e, por consequência, o seu perfil.
        request.user.delete()
        messages.success(request, 'A sua conta foi apagada com sucesso.')
        return redirect('logout')

    return render(request, 'usuario/apagar_usuario.html')
