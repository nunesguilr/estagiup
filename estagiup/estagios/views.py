from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import Estagio
from .forms import EstagioForm

def estagio_list(request):
    estagios = Estagio.objects.all()
    return render(request, 'estagios/estagio_list.html', {'estagios': estagios})

def estagio_detail(request, pk):
    estagio = get_object_or_404(Estagio, pk=pk)
    return render(request, 'estagios/estagio_detail.html', {'estagio': estagio})

def estagio_create(request):
    if request.method == 'POST':
        form = EstagioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estágio criado com sucesso!')
            return redirect('estagio_list')
    else:
        form = EstagioForm()
    return render(request, 'estagios/estagio_form.html', {'form': form})

def estagio_update(request, pk):
    estagio = get_object_or_404(Estagio, pk=pk)
    if request.method == 'POST':
        form = EstagioForm(request.POST, instance=estagio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estágio atualizado com sucesso!')
            return redirect('estagio_detail', pk=pk)
    else:
        form = EstagioForm(instance=estagio)
    return render(request, 'estagios/estagio_form.html', {'form': form})

def estagio_delete(request, pk):
    estagio = get_object_or_404(Estagio, pk=pk)
    if request.method == 'POST':
        estagio.delete()
        messages.success(request, 'Estágio excluído com sucesso!')
        return redirect('estagio_list')
    return render(request, 'estagios/estagio_confirm_delete.html', {'estagio': estagio})

def estagio_concluir(request, pk):
    estagio = get_object_or_404(Estagio, pk=pk)
    if request.method == 'POST':
        estagio.status = 'concluido'
        estagio.save()
        messages.success(request, f'Estágio "{estagio.id}" marcado como Concluído.')
    return redirect('estagio_detail', pk=pk)

def estagio_cancelar(request, pk):
    estagio = get_object_or_404(Estagio, pk=pk)
    if request.method == 'POST':
        estagio.status = 'cancelado'
        estagio.save()
        messages.warning(request, f'Estágio "{estagio.id}" marcado como Cancelado.')
    return redirect('estagio_detail', pk=pk)
