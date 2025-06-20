from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import Vaga
from .forms import VagaForm

def vaga_list(request):
    vagas = Vaga.objects.all()
    return render(request, 'vagas/vaga_list.html', {'vagas': vagas})

def vaga_detail(request, pk):
    vaga = get_object_or_404(Vaga, pk=pk)
    return render(request, 'vagas/vaga_detail.html', {'vaga': vaga})

def vaga_create(request):
    if request.method == 'POST':
        form = VagaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vaga criada com sucesso!')
            return redirect('vaga_list')
    else:
        form = VagaForm()
    return render(request, 'vagas/vaga_form.html', {'form': form})

def vaga_update(request, pk):
    vaga = get_object_or_404(Vaga, pk=pk)
    if request.method == 'POST':
        form = VagaForm(request.POST, instance=vaga)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vaga atualizada com sucesso!')
            return redirect('vaga_detail', pk=pk)
    else:
        form = VagaForm(instance=vaga)
    return render(request, 'vagas/vaga_form.html', {'form': form})

def vaga_delete(request, pk):
    vaga = get_object_or_404(Vaga, pk=pk)
    if request.method == 'POST':
        vaga.delete()
        messages.success(request, 'Vaga excluída com sucesso!')
        return redirect('vaga_list')
    return render(request, 'vagas/vaga_confirm_delete.html', {'vaga': vaga})

def vaga_apply(request, pk):
    vaga = get_object_or_404(Vaga, pk=pk)
    messages.success(request, f'Lógica de candidatura para a vaga "{vaga.titulo}" seria implementada aqui!')
    return redirect('vaga_detail', pk=pk)
