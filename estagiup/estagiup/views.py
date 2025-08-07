from django.shortcuts import render

def index(request):

    context = {}
    return render(request, 'index.html', {'message': 'Bem-vindo ao EstagiUP!'})
    
def sobre_view(request):
    # Esta view por enquanto só precisa mostrar a página
    return render(request, 'sobre.html')

def dashboard_view(request):
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

