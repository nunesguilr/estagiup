from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from .models import Nota, Relatorio
from .forms import NotaForm, RelatorioForm
from estagios.models import Estagio

def nota_list(request):
    notas = Nota.objects.all()
    return render(request, 'avaliacoes/nota_list.html', {'notas': notas})

def nota_detail(request, pk):
    nota = get_object_or_404(Nota, pk=pk)
    return render(request, 'avaliacoes/nota_detail.html', {'nota': nota})

def nota_create(request, estagio_pk):
    estagio = get_object_or_404(Estagio, pk=estagio_pk)
    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.estagio = estagio
            nota.save()
            messages.success(request, 'Nota criada com sucesso!')
            return redirect('nota_list')
    else:
        form = NotaForm(initial={'estagio': estagio})
    return render(request, 'avaliacoes/nota_form.html', {'form': form, 'estagio': estagio})

def nota_update(request, pk):
    nota = get_object_or_404(Nota, pk=pk)
    if request.method == 'POST':
        form = NotaForm(request.POST, instance=nota)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nota atualizada com sucesso!')
            return redirect('nota_detail', pk=pk)
    else:
        form = NotaForm(instance=nota)
    return render(request, 'avaliacoes/nota_form.html', {'form': form})

def nota_delete(request, pk):
    nota = get_object_or_404(Nota, pk=pk)
    if request.method == 'POST':
        nota.delete()
        messages.success(request, 'Nota excluída com sucesso!')
        return redirect('nota_list')
    return render(request, 'avaliacoes/nota_confirm_delete.html', {'nota': nota})

def relatorio_list(request):
    relatorios = Relatorio.objects.all()
    return render(request, 'avaliacoes/relatorio_list.html', {'relatorios': relatorios})

def relatorio_detail(request, pk):
    relatorio = get_object_or_404(Relatorio, pk=pk)
    return render(request, 'avaliacoes/relatorio_detail.html', {'relatorio': relatorio})

def relatorio_create(request, estagio_pk):
    estagio = get_object_or_404(Estagio, pk=estagio_pk)
    if request.method == 'POST':
        form = RelatorioForm(request.POST)
        if form.is_valid():
            relatorio = form.save(commit=False)
            relatorio.estagio = estagio
            relatorio.save()
            messages.success(request, 'Relatório criado com sucesso!')
            return redirect('relatorio_list')
    else:
        form = RelatorioForm(initial={'estagio': estagio})
    return render(request, 'avaliacoes/relatorio_form.html', {'form': form, 'estagio': estagio})

def relatorio_update(request, pk):
    relatorio = get_object_or_404(Relatorio, pk=pk)
    if request.method == 'POST':
        form = RelatorioForm(request.POST, instance=relatorio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Relatório atualizado com sucesso!')
            return redirect('relatorio_detail', pk=pk)
    else:
        form = RelatorioForm(instance=relatorio)
    return render(request, 'avaliacoes/relatorio_form.html', {'form': form})

def relatorio_salvar_rascunho(request, pk):
    relatorio = get_object_or_404(Relatorio, pk=pk)
    if request.method == 'POST':
        new_content = request.POST.get('conteudo', '')
        relatorio.conteudo = new_content
        relatorio.save()
        return JsonResponse({'status': 'success', 'message': 'Rascunho salvo com sucesso!'})
    return JsonResponse({'status': 'error', 'message': 'Método não permitido.'}, status=405)

def relatorio_enviar(request, pk):
    relatorio = get_object_or_404(Relatorio, pk=pk)
    if request.method == 'POST':
        if relatorio.status == 'enviado' or relatorio.status == 'avaliado':
            nova_versao = Relatorio.objects.create(
                estagio=relatorio.estagio,
                conteudo=relatorio.conteudo,
                validade=relatorio.validade,
                status='enviado',
                versao=relatorio.versao + 1
            )
            messages.success(request, f'Nova versão do relatório ({nova_versao.versao}) enviada com sucesso!')
            return redirect('relatorio_detail', pk=nova_versao.pk)
        else:
            relatorio.status = 'enviado'
            relatorio.save()
            messages.success(request, 'Relatório enviado com sucesso!')
        return redirect('relatorio_detail', pk=pk)
    return redirect('relatorio_detail', pk=pk)

def relatorio_historico(request, pk):
    original_relatorio = get_object_or_404(Relatorio, pk=pk)
    versoes_relatorio = Relatorio.objects.filter(estagio=original_relatorio.estagio).order_by('versao')
    return render(request, 'avaliacoes/relatorio_historico.html', {'versoes_relatorio': versoes_relatorio, 'original_relatorio': original_relatorio})

def relatorio_avaliar(request, pk):
    relatorio = get_object_or_404(Relatorio, pk=pk)
    if request.method == 'POST':
        avaliacao_valor = request.POST.get('avaliacao_valor')
        if avaliacao_valor:
            relatorio.avaliacao = float(avaliacao_valor)
            relatorio.status = 'avaliado'
            relatorio.save()
            messages.success(request, f'Relatório avaliado com sucesso: {avaliacao_valor}.')
        else:
            messages.error(request, 'Valor de avaliação não fornecido.')
        return redirect('relatorio_detail', pk=pk)
    return redirect('relatorio_detail', pk=pk)

def relatorio_delete(request, pk):
    relatorio = get_object_or_404(Relatorio, pk=pk)
    if request.method == 'POST':
        relatorio.delete()
        messages.success(request, 'Relatório excluído com sucesso!')
        return redirect('relatorio_list')
    return render(request, 'avaliacoes/relatorio_confirm_delete.html', {'relatorio': relatorio})
