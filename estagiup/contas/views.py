from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import Usuario, Aluno, ContaEmpresa, Supervisor, Professor, ContaInstituicao
from .forms import UsuarioForm, AlunoForm, ContaEmpresaForm, SupervisorForm, ProfessorForm, ContaInstituicaoForm

def usuario_list(request):
    usuarios = Usuario.objects.all()
    return render(request, 'contas/usuario_list.html', {'usuarios': usuarios})

def usuario_detail(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    return render(request, 'contas/usuario_detail.html', {'usuario': usuario})

def usuario_create(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('usuario_list')
    else:
        form = UsuarioForm()
    return render(request, 'contas/usuario_form.html', {'form': form})

def usuario_update(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('usuario_detail', pk=pk)
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'contas/usuario_form.html', {'form': form})

def usuario_delete(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuário excluído com sucesso!')
        return redirect('usuario_list')
    return render(request, 'contas/usuario_confirm_delete.html', {'usuario': usuario})

def aluno_list(request):
    alunos = Aluno.objects.all()
    return render(request, 'contas/aluno_list.html', {'alunos': alunos})

def aluno_detail(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    return render(request, 'contas/aluno_detail.html', {'aluno': aluno})

def aluno_create(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aluno criado com sucesso!')
            return redirect('aluno_list')
    else:
        form = AlunoForm()
    return render(request, 'contas/aluno_form.html', {'form': form})

def aluno_update(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aluno atualizado com sucesso!')
            return redirect('aluno_detail', pk=pk)
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'contas/aluno_form.html', {'form': form})

def aluno_delete(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == 'POST':
        aluno.delete()
        messages.success(request, 'Aluno excluído com sucesso!')
        return redirect('aluno_list')
    return render(request, 'contas/aluno_confirm_delete.html', {'aluno': aluno})

def empresa_list(request):
    empresas = ContaEmpresa.objects.all()
    return render(request, 'contas/empresa_list.html', {'empresas': empresas})

def empresa_detail(request, pk):
    empresa = get_object_or_404(ContaEmpresa, pk=pk)
    return render(request, 'contas/empresa_detail.html', {'empresa': empresa})

def empresa_create(request):
    if request.method == 'POST':
        form = ContaEmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa criada com sucesso!')
            return redirect('empresa_list')
    else:
        form = ContaEmpresaForm()
    return render(request, 'contas/empresa_form.html', {'form': form})

def empresa_update(request, pk):
    empresa = get_object_or_404(ContaEmpresa, pk=pk)
    if request.method == 'POST':
        form = ContaEmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa atualizada com sucesso!')
            return redirect('empresa_detail', pk=pk)
    else:
        form = ContaEmpresaForm(instance=empresa)
    return render(request, 'contas/empresa_form.html', {'form': form})

def empresa_delete(request, pk):
    empresa = get_object_or_404(ContaEmpresa, pk=pk)
    if request.method == 'POST':
        empresa.delete()
        messages.success(request, 'Empresa excluída com sucesso!')
        return redirect('empresa_list')
    return render(request, 'contas/empresa_confirm_delete.html', {'empresa': empresa})

def supervisor_list(request):
    supervisores = Supervisor.objects.all()
    return render(request, 'contas/supervisor_list.html', {'supervisores': supervisores})

def supervisor_detail(request, pk):
    supervisor = get_object_or_404(Supervisor, pk=pk)
    return render(request, 'contas/supervisor_detail.html', {'supervisor': supervisor})

def supervisor_create(request):
    if request.method == 'POST':
        form = SupervisorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supervisor criado com sucesso!')
            return redirect('supervisor_list')
    else:
        form = SupervisorForm()
    return render(request, 'contas/supervisor_form.html', {'form': form})

def supervisor_update(request, pk):
    supervisor = get_object_or_404(Supervisor, pk=pk)
    if request.method == 'POST':
        form = SupervisorForm(request.POST, instance=supervisor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supervisor atualizado com sucesso!')
            return redirect('supervisor_detail', pk=pk)
    else:
        form = SupervisorForm(instance=supervisor)
    return render(request, 'contas/supervisor_form.html', {'form': form})

def supervisor_delete(request, pk):
    supervisor = get_object_or_404(Supervisor, pk=pk)
    if request.method == 'POST':
        supervisor.delete()
        messages.success(request, 'Supervisor excluído com sucesso!')
        return redirect('supervisor_list')
    return render(request, 'contas/supervisor_confirm_delete.html', {'supervisor': supervisor})

def professor_list(request):
    professores = Professor.objects.all()
    return render(request, 'contas/professor_list.html', {'professores': professores})

def professor_detail(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    return render(request, 'contas/professor_detail.html', {'professor': professor})

def professor_create(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Professor criado com sucesso!')
            return redirect('professor_list')
    else:
        form = ProfessorForm()
    return render(request, 'contas/professor_form.html', {'form': form})

def professor_update(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    if request.method == 'POST':
        form = ProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Professor atualizado com sucesso!')
            return redirect('professor_detail', pk=pk)
    else:
        form = ProfessorForm(instance=professor)
    return render(request, 'contas/professor_form.html', {'form': form})

def professor_delete(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    if request.method == 'POST':
        professor.delete()
        messages.success(request, 'Professor excluído com sucesso!')
        return redirect('professor_list')
    return render(request, 'contas/professor_confirm_delete.html', {'professor': professor})

def instituicao_list(request):
    instituicoes = ContaInstituicao.objects.all()
    return render(request, 'contas/instituicao_list.html', {'instituicoes': instituicoes})

def instituicao_detail(request, pk):
    instituicao = get_object_or_404(ContaInstituicao, pk=pk)
    return render(request, 'contas/instituicao_detail.html', {'instituicao': instituicao})

def instituicao_create(request):
    if request.method == 'POST':
        form = ContaInstituicaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Instituição criada com sucesso!')
            return redirect('instituicao_list')
    else:
        form = ContaInstituicaoForm()
    return render(request, 'contas/instituicao_form.html', {'form': form})

def instituicao_update(request, pk):
    instituicao = get_object_or_404(ContaInstituicao, pk=pk)
    if request.method == 'POST':
        form = ContaInstituicaoForm(request.POST, instance=instituicao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Instituição atualizada com sucesso!')
            return redirect('instituicao_detail', pk=pk)
    else:
        form = ContaInstituicaoForm(instance=instituicao)
    return render(request, 'contas/instituicao_form.html', {'form': form})

def instituicao_delete(request, pk):
    instituicao = get_object_or_404(ContaInstituicao, pk=pk)
    if request.method == 'POST':
        instituicao.delete()
        messages.success(request, 'Instituição excluída com sucesso!')
        return redirect('instituicao_list')
    return render(request, 'contas/instituicao_confirm_delete.html', {'instituicao': instituicao})
