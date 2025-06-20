from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import Curso
from .forms import CursoForm

def curso_list(request):
    cursos = Curso.objects.all()
    return render(request, 'cursos/curso_list.html', {'cursos': cursos})

def curso_detail(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    return render(request, 'cursos/curso_detail.html', {'curso': curso})

def curso_create(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso criado com sucesso!')
            return redirect('curso_list')
    else:
        form = CursoForm()
    return render(request, 'cursos/curso_form.html', {'form': form})

def curso_update(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso atualizado com sucesso!')
            return redirect('curso_detail', pk=pk)
    else:
        form = CursoForm(instance=curso)
    return render(request, 'cursos/curso_form.html', {'form': form})

def curso_delete(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        curso.delete()
        messages.success(request, 'Curso excluído com sucesso!')
        return redirect('curso_list')
    return render(request, 'cursos/curso_confirm_delete.html', {'curso': curso})
