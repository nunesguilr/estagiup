# curso/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import Curso
from .forms import CursoForm

@login_required
def curso_list(request):
    """
    Lista todos os cursos.
    """
    cursos = Curso.objects.all()
    context = {
        'cursos': cursos
    }
    return render(request, 'curso/curso_list.html', context)


@login_required
def curso_detail(request, curso_id):
    """
    Exibe os detalhes de um curso específico.
    """
    curso = get_object_or_404(Curso, id=curso_id)
    context = {
        'curso': curso
    }
    return render(request, 'curso/curso_detail.html', context)


@login_required
@permission_required('curso.add_curso', raise_exception=True)
def curso_create(request):
    """
    View para o cadastro de um novo curso.
    """
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso cadastrado com sucesso!')
            return redirect('curso:curso_list')
        else:
            messages.error(request, 'Erro ao cadastrar o curso. Por favor, verifique os campos.')
    else:
        form = CursoForm()

    context = {
        'form': form
    }
    return render(request, 'curso/curso_form.html', context)


@login_required
@permission_required('curso.change_curso', raise_exception=True)
def curso_update(request, curso_id):
    """
    Permite editar os dados de um curso.
    """
    curso = get_object_or_404(Curso, id=curso_id)
    
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, f'Curso "{curso.nome}" atualizado com sucesso!')
            return redirect('curso:curso_detail', curso_id=curso.id)
        else:
            messages.error(request, 'Erro ao atualizar o curso. Por favor, verifique os campos.')
    else:
        form = CursoForm(instance=curso)

    context = {
        'form': form,
        'curso': curso
    }
    return render(request, 'curso/curso_form.html', context)


@login_required
@permission_required('curso.delete_curso', raise_exception=True)
def curso_delete(request, curso_id):
    """
    Permite apagar um curso.
    """
    curso = get_object_or_404(Curso, id=curso_id)

    if request.method == 'POST':
        curso.delete()
        messages.success(request, f'Curso "{curso.nome}" apagado com sucesso.')
        return redirect('curso:curso_list')
        
    context = {
        'curso': curso
    }
    return render(request, 'curso/curso_confirm_delete.html', context)
