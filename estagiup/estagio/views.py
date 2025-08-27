# estagio/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import Estagio, Vaga
from .forms import EstagioForm
from usuario.models import PerfilUsuario
from django.contrib.auth.models import Group
from datetime import date, timedelta

@login_required
def estagio_list(request):
    """
    Lista todos os estágios. A visibilidade é filtrada por permissão e papel do usuário.
    """
    estagios = Estagio.objects.all().select_related('aluno', 'vaga', 'supervisor', 'orientador')
    
    # Lógica de filtro para cada tipo de usuário
    try:
        if not request.user.is_superuser:
            perfil_usuario = request.user.perfil
            grupos = [grupo.name for grupo in request.user.groups.all()]
            
            if 'Alunos' in grupos:
                estagios = estagios.filter(aluno=perfil_usuario)
            elif 'Supervisores' in grupos:
                estagios = estagios.filter(supervisor=perfil_usuario)
            elif 'Orientadores' in grupos:
                estagios = estagios.filter(orientador=perfil_usuario)
            else:
                estagios = Estagio.objects.none() # Não exibe nada para outros grupos
    except PerfilUsuario.DoesNotExist:
        estagios = Estagio.objects.none()

    # Lógica para calcular a porcentagem de progresso
    hoje = date.today()
    for estagio in estagios:
        if estagio.status == 'ativo' and estagio.dt_ini and estagio.dt_fim:
            total_dias = (estagio.dt_fim - estagio.dt_ini).days
            dias_passados = (hoje - estagio.dt_ini).days
            if total_dias > 0:
                progresso = (dias_passados / total_dias) * 100
                if progresso > 100:
                    progresso = 100
                estagio.progresso = progresso
            else:
                estagio.progresso = 0
        else:
            estagio.progresso = 0

    context = {
        'estagios': estagios
    }
    return render(request, 'estagio/estagio_list.html', context)


@login_required
def estagio_detail(request, estagio_id):
    """
    Exibe os detalhes de um estágio específico.
    """
    estagio = get_object_or_404(Estagio, id=estagio_id)
    
    # Verifica se o usuário tem permissão para visualizar o estágio
    grupos = [grupo.name for grupo in request.user.groups.all()]
    if (not request.user.is_superuser and
        'Alunos' in grupos and estagio.aluno != request.user.perfil or
        'Supervisores' in grupos and estagio.supervisor != request.user.perfil or
        'Orientadores' in grupos and estagio.orientador != request.user.perfil):
        messages.error(request, 'Você não tem permissão para visualizar este estágio.')
        return redirect('estagio:estagio_list')

    # Adicionando o campo `can_edit` ao contexto
    can_edit = False
    if hasattr(request.user, 'perfil') and (request.user.perfil == estagio.supervisor or request.user.perfil == estagio.orientador or request.user.is_superuser):
        can_edit = True

    context = {
        'estagio': estagio,
        'can_edit': can_edit
    }
    return render(request, 'estagio/estagio_detail.html', context)


@login_required
@permission_required('estagio.add_estagio', raise_exception=True)
def estagio_create(request, vaga_id):
    """
    View para o cadastro de um novo estágio (candidatura).
    """
    vaga = get_object_or_404(Vaga, id=vaga_id)
    
    try:
        perfil_aluno = request.user.perfil
    except PerfilUsuario.DoesNotExist:
        messages.error(request, 'O seu utilizador não tem um perfil de aluno válido.')
        return redirect('vaga:vaga_list')

    if Estagio.objects.filter(aluno=perfil_aluno).exists():
        messages.error(request, 'Você já está cadastrado em um estágio.')
        return redirect('estagio:estagio_list')
    
    # Lógica para filtrar as opções de supervisor e orientador
    supervisores_group = Group.objects.get(name='Supervisores')
    orientadores_group = Group.objects.get(name='Orientadores')

    if request.method == 'POST':
        form = EstagioForm(request.POST)
        if form.is_valid():
            estagio = form.save(commit=False)
            estagio.aluno = perfil_aluno
            estagio.vaga = vaga
            estagio.nota = 0  # Define a nota inicial como 0
            estagio.save()
            messages.success(request, f'Candidatura para a vaga "{vaga.titulo}" enviada com sucesso!')
            return redirect('estagio:estagio_list')
        else:
            messages.error(request, 'Erro ao enviar a candidatura. Por favor, verifique os campos.')
    else:
        form = EstagioForm()

    # Remove o campo 'nota' do formulário de criação
    del form.fields['nota']
    # Restringe o queryset dos campos `supervisor` e `orientador`
    form.fields['supervisor'].queryset = PerfilUsuario.objects.filter(user__groups=supervisores_group)
    form.fields['orientador'].queryset = PerfilUsuario.objects.filter(user__groups=orientadores_group)

    context = {
        'form': form,
        'vaga': vaga
    }
    return render(request, 'estagio/estagio_form.html', context)


@login_required
@permission_required('estagio.change_estagio', raise_exception=True)
def estagio_update(request, estagio_id):
    """
    Permite que o supervisor/orientador edite um estágio.
    """
    estagio = get_object_or_404(Estagio, id=estagio_id)
    
    if request.user.perfil not in [estagio.supervisor, estagio.orientador] and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para editar este estágio.')
        return redirect('estagio:estagio_detail', estagio_id=estagio.id)

    # Lógica para filtrar as opções de supervisor e orientador
    supervisores_group = Group.objects.get(name='Supervisores')
    orientadores_group = Group.objects.get(name='Orientadores')

    if request.method == 'POST':
        form = EstagioForm(request.POST, instance=estagio)
        if form.is_valid():
            form.save()
            messages.success(request, f'Estágio de "{estagio.aluno.user.username}" atualizado com sucesso!')
            return redirect('estagio:estagio_detail', estagio_id=estagio.id)
        else:
            messages.error(request, 'Erro ao atualizar o estágio. Por favor, verifique os campos.')
    else:
        form = EstagioForm(instance=estagio)

    # Restringe o queryset dos campos `supervisor` e `orientador`
    form.fields['supervisor'].queryset = PerfilUsuario.objects.filter(user__groups=supervisores_group)
    form.fields['orientador'].queryset = PerfilUsuario.objects.filter(user__groups=orientadores_group)

    # Verifica se o usuário é supervisor ou superusuário
    is_supervisor_or_superuser = 'Supervisores' in [group.name for group in request.user.groups.all()] or request.user.is_superuser
    
    # Se não for supervisor ou superusuário, remove o campo 'nota' do formulário
    if not is_supervisor_or_superuser:
        del form.fields['nota']

    context = {
        'form': form,
        'estagio': estagio
    }
    return render(request, 'estagio/estagio_form.html', context)


@login_required
def estagio_delete(request, estagio_id):
    """
    Permite apagar um estágio. Apenas admins, supervisores ou o próprio aluno.
    """
    estagio = get_object_or_404(Estagio, id=estagio_id)
    
    # Adicionando a verificação de permissão para o aluno que é dono do estágio
    if (request.user.perfil != estagio.supervisor and 
        request.user.perfil != estagio.aluno and 
        not request.user.is_superuser):
        messages.error(request, 'Você não tem permissão para apagar este estágio.')
        return redirect('estagio:estagio_detail', estagio_id=estagio.id)

    if request.method == 'POST':
        estagio.delete()
        messages.success(request, f'Estágio de "{estagio.aluno.user.username}" apagado com sucesso.')
        return redirect('estagio:estagio_list')
        
    context = {
        'estagio': estagio
    }
    return render(request, 'estagio/estagio_confirm_delete.html', context)
