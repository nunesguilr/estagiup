# usuario/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm
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
            return redirect('usuario:login')
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
