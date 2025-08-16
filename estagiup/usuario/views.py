# usuario/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegistrationForm, UserAuthenticationForm
from .models import PerfilUsuario
from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User # Importe o modelo User

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
        form = UserAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bem-vindo(a) de volta, {user.username}!')
            return redirect('dashboard')
    else:
        form = UserAuthenticationForm()

    context = {
        'form': form
    }
    return render(request, 'usuario/login.html', context)

def lista_usuarios(request):
    """
    View para exibir uma lista de todos os utilizadores e seus perfis.
    """
    todos_usuarios = PerfilUsuario.objects.all().select_related('user').order_by('user__username')
    todos_grupos = Group.objects.all()
    context = {
        'todos_usuarios': todos_usuarios
    }
    return render(request, 'usuario/lista.html', context)

def user_detail_view(request, user_id):
    # Busca o usuário pelo ID ou retorna um erro 404 se não encontrar
    target_user = get_object_or_404(User, pk=user_id)

    context = {
        'target_user': target_user
    }
    return render(request, 'usuario/user_detail.html', context)