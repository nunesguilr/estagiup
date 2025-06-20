from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import Notificacao

def notificacao_list(request):
    notificacoes = Notificacao.objects.all()
    if request.user.is_authenticated and hasattr(request.user, 'usuario'):
        notificacoes = Notificacao.objects.filter(destinatario=request.user.usuario)
    else:
        notificacoes = Notificacao.objects.none()
    return render(request, 'notificacoes/notificacao_list.html', {'notificacoes': notificacoes})

def notificacao_detail(request, pk):
    notificacao = get_object_or_404(Notificacao, pk=pk)
    if not notificacao.lido:
        notificacao.lido = True
        notificacao.save()
    return render(request, 'notificacoes/notificacao_detail.html', {'notificacao': notificacao})

def notificacao_marcar_lida(request, pk):
    notificacao = get_object_or_404(Notificacao, pk=pk)
    if request.method == 'POST':
        notificacao.lido = True
        notificacao.save()
        messages.success(request, 'Notificação marcada como lida.')
    return redirect('notificacao_list')
