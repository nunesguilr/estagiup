from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Vaga
# Assumindo que você tem um forms.py no app vaga
# from .forms import VagaForm 

# View para listar todas as vagas
def vaga_list(request):
    vagas = Vaga.objects.all()
    return render(request, 'vagas/vaga_list.html', {'vagas': vagas})

# View para ver os detalhes de uma vaga específica
def vaga_detail(request, pk):
    vaga = get_object_or_404(Vaga, pk=pk)
    return render(request, 'vagas/vaga_detail.html', {'vaga': vaga})

# View para criar uma nova vaga (exemplo, pode não ter o VagaForm ainda)
def vaga_create(request):
    # A lógica para criar uma vaga com formulário viria aqui
    # if request.method == 'POST':
    #     form = VagaForm(request.POST)
    #     ...
    # else:
    #     form = VagaForm()
    # return render(request, 'vagas/vaga_form.html', {'form': form})
    messages.info(request, 'A página para criar vagas ainda será implementada.')
    return redirect('vaga:vaga_list') # Redireciona de volta para a lista

# E assim por diante para as outras funções de update, delete, etc.