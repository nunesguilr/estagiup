from django.urls import path
from . import views

app_name = 'vaga'

urlpatterns = [
    # URL para a visualização pública de vagas
    path('', views.vaga_public, name='vaga_public'),
    
    # URL para a listagem interna (gerenciamento) de vagas
    path('listar/', views.vaga_list, name='vaga_list'),
    
    path('adicionar/', views.vaga_create, name='vaga_create'),
    path('<int:vaga_id>/', views.vaga_detail, name='vaga_detail'),
    path('<int:vaga_id>/editar/', views.vaga_update, name='vaga_update'),
    path('<int:vaga_id>/apagar/', views.vaga_delete, name='vaga_delete'),
]
