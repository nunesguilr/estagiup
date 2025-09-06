from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Estagio, Vaga
from .forms import EstagioForm
from usuario.models import Usuario
from django.contrib.auth.models import Group
from datetime import date

@login_required
def estagio_list(request):
    """
    Lista todos os estágios. A visibilidade é filtrada por permissão e papel do usuário.
    """
    estagios = Estagio.objects.all().select_related('aluno', 'vaga', 'supervisor', 'orientador')
    
    # Lógica de filtro para cada tipo de usuário
    if not request.user.is_superuser:
        grupos = [grupo.name for grupo in request.user.groups.all()]
        
        if 'Alunos' in grupos:
            estagios = estagios.filter(aluno=request.user)
        elif 'Supervisores' in grupos:
            estagios = estagios.filter(supervisor=request.user)
        elif 'Orientadores' in grupos:
            estagios = estagios.filter(orientador=request.user)
        else:
            estagios = Estagio.objects.none() # Não exibe nada para outros grupos

    # Lógica para calcular a porcentagem de progresso
    hoje = date.today()
    for estagio in estagios:
        # Verifica se o status é True (ativo)
        if estagio.status and estagio.dt_ini and estagio.dt_fim:
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
        'Alunos' in grupos and estagio.aluno != request.user or
        'Supervisores' in grupos and estagio.supervisor != request.user or
        'Orientadores' in grupos and estagio.orientador != request.user):
        return redirect('estagio:estagio_list')

    # Adicionando o campo `can_edit` ao contexto
    can_edit = False
    if (request.user == estagio.supervisor or request.user == estagio.orientador or request.user.is_superuser):
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
    
    perfil_aluno = request.user
    
    if Estagio.objects.filter(aluno=perfil_aluno).exists():
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
            return redirect('estagio:estagio_list')
        else:
            pass
    else:
        form = EstagioForm()

    # Remove o campo 'nota' do formulário de criação
    del form.fields['nota']
    # Restringe o queryset dos campos `supervisor` e `orientador`
    form.fields['supervisor'].queryset = Usuario.objects.filter(groups=supervisores_group)
    form.fields['orientador'].queryset = Usuario.objects.filter(groups=orientadores_group)

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
    
    if request.user not in [estagio.supervisor, estagio.orientador] and not request.user.is_superuser:
        return redirect('estagio:estagio_detail', estagio_id=estagio.id)

    # Lógica para filtrar as opções de supervisor e orientador
    supervisores_group = Group.objects.get(name='Supervisores')
    orientadores_group = Group.objects.get(name='Orientadores')

    if request.method == 'POST':
        form = EstagioForm(request.POST, instance=estagio)
        if form.is_valid():
            form.save()
            return redirect('estagio:estagio_detail', estagio_id=estagio.id)
        else:
            pass
    else:
        form = EstagioForm(instance=estagio)

    # Restringe o queryset dos campos `supervisor` e `orientador`
    form.fields['supervisor'].queryset = Usuario.objects.filter(groups=supervisores_group)
    form.fields['orientador'].queryset = Usuario.objects.filter(groups=orientadores_group)

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
    if (request.user != estagio.supervisor and 
        request.user != estagio.aluno and 
        not request.user.is_superuser):
        return redirect('estagio:estagio_detail', estagio_id=estagio.id)

    if request.method == 'POST':
        estagio.delete()
        return redirect('estagio:estagio_list')
        
    context = {
        'estagio': estagio
    }
    return render(request, 'estagio/estagio_confirm_delete.html', context)
