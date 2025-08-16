from django.shortcuts import render
# from django.contrib.auth.decorators import login_required # Usaremos no futuro

def index(request):

    context = {}
    return render(request, 'index.html', {'message': 'Bem-vindo ao EstagiUP!'})
    
def sobre_view(request):
    # Esta view por enquanto só precisa mostrar a página
    return render(request, 'sobre.html')

# @login_required
def dashboard_view(request):
    # Por enquanto, vamos simular que o usuário é um aluno
    # NO FUTURO:
    # if request.user.groups.filter(name='Aluno Cursando').exists():
    #     # Lógica e contexto para o aluno
    #     return render(request, 'usuario/dashboard_aluno.html', context)
    # elif request.user.groups.filter(name='Supervisor da Empresa').exists():
    #     # Lógica e contexto para a empresa
    #     return render(request, 'usuario/dashboard_empresa.html', context)
    # ... e assim por diante

    # POR AGORA, VAMOS APENAS RENDERIZAR O NOVO DASHBOARD DO ALUNO
    return render(request, 'aluno/dashboard_aluno.html')

def vagas_exemplo(request):
    # No futuro, estes dados virão do banco de dados de verdade.
    # Por agora, é só um exemplo para o template funcionar.
    vagas_exemplo = [
        {
            'titulo': 'Desenvolvedor(a) Frontend',
            'descricao': 'Empresa XYZ está buscando um desenvolvedor frontend para trabalhar em projetos inovadores. Requisitos: HTML, CSS, JavaScript.'
        },
        {
            'titulo': 'Analista de Marketing Digital',
            'descricao': 'Procura-se um analista de marketing digital para gerenciar campanhas online. Requisitos: SEO, Google Ads, Redes Sociais.'
        },
        {
            'titulo': 'Estagiário em Design Gráfico',
            'descricao': 'Aplicação Criativa está em busca de um estagiário em design gráfico. Requisitos: Photoshop, Illustrator, Criatividade.'
        },
    ]

    context = {
        'ultimas_vagas': vagas_exemplo
    }
    return render(request, 'dashboard.html', context)

