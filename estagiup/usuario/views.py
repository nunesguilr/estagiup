from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, PerfilUpdateForm
from .models import PerfilUsuario

def registrar_usuario(request):
    """
    View para registar um novo utilizador, seu perfil e atribuí-lo a um grupo.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Bem-vindo(a), {user.username}! O seu registo foi concluído com sucesso.')
            return redirect('login')
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
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bem-vindo(a) de volta, {user.username}!')
            return redirect('dashboard')
        else:
            form = AuthenticationForm()

    context = {
        'form': form
    }
    return render(request, 'usuario/login.html', context)

def lista_usuarios(request):
    """
    View para exibir uma lista de todos os utilizadores e seus perfis.
    """
    todos_usuarios = PerfilUsuario.objects.all().select_related('user').order_by('user__username')
    context = {
        'todos_usuarios': todos_usuarios
    }
    return render(request, 'usuario/lista.html', context)

@login_required
def user_detail(request, pk):
    """
    View para exibir os detalhes de um utilizador específico.
    """
    target_user = get_object_or_404(User.objects.select_related('perfil'), pk=pk)
    context = {
        'target_user': target_user
    }
    return render(request, 'usuario/user_detail.html', context)


@login_required
def editar_perfil(request):
    """
    View para que o utilizador logado edite o seu próprio perfil.
    """
    try:
        perfil = request.user.perfil
    except PerfilUsuario.DoesNotExist:
        messages.error(request, 'O seu utilizador não tem um perfil associado.')
        return redirect('dashboard')

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
def apagar_usuario(request, pk):
    """
    View para apagar um utilizador específico (requer permissões de admin).
    """
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para apagar utilizadores.')
        return redirect('dashboard')
    
    user_to_delete = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        user_to_delete.delete()
        messages.success(request, f'A conta de {user_to_delete.username} foi apagada com sucesso.')
        return redirect('usuario:lista_usuarios')
    
    context = {
        'target_user': user_to_delete
    }
    return render(request, 'usuario/apagar_confirmar.html', context)
from .forms import UserRegistrationForm, PerfilUpdateForm
from .models import PerfilUsuario

def registrar_usuario(request):
    """
    View para registar um novo utilizador, seu perfil e atribuí-lo a um grupo.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Bem-vindo(a), {user.username}! O seu registo foi concluído com sucesso.')
            return redirect('login')
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
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bem-vindo(a) de volta, {user.username}!')
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    context = {
        'form': form
    }
    return render(request, 'usuario/login.html', context)

def lista_usuarios(request):
    """
    View para exibir uma lista de todos os utilizadores e seus perfis.
    """
    todos_usuarios = PerfilUsuario.objects.all().select_related('user').order_by('user__username')
    context = {
        'todos_usuarios': todos_usuarios
    }
    return render(request, 'usuario/lista.html', context)

@login_required
def editar_perfil(request):
    """
    View para que o utilizador logado edite o seu próprio perfil.
    """
    try:
        perfil = request.user.perfil
    except PerfilUsuario.DoesNotExist:
        messages.error(request, 'O seu utilizador não tem um perfil associado.')
        return redirect('dashboard')

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
        return redirect('login')
    
    return render(request, 'usuario/apagar_usuario.html')

