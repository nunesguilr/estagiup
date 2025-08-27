from django.urls import path
from . import views

app_name = 'vaga'

urlpatterns = [
    # URL para a visualização pública de vagas
    path('', views.vaga_public, name='vaga_public'),
    path('publico/<int:vaga_id>/', views.vaga_public_detail, name='vaga_public_detail'),
    
    # URL para a listagem interna (gerenciamento) de vagas
    path('listar/', views.vaga_list, name='vaga_list'),
    
    path('select-instituicao/', views.selecionar_instituicao_para_vaga, name='selecionar_instituicao_para_vaga'),
    path('<int:instituicao_id>/adicionar/', views.vaga_create, name='vaga_create'),
    path('<int:vaga_id>/', views.vaga_detail, name='vaga_detail'),
    path('<int:vaga_id>/editar/', views.vaga_update, name='vaga_update'),
    path('<int:vaga_id>/apagar/', views.vaga_delete, name='vaga_delete'),
]
