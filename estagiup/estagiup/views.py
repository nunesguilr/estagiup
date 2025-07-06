from django.shortcuts import render

def index(request):

    context = {}
    return render(request, 'index.html', {'message': 'Bem-vindo ao EstagiUP!'})
    
def dashboard_view(request):
    # No futuro, aqui terá lógica para pegar dados do usuário logado
    return render(request, 'dashboard.html')