from django.urls import path
from . import views

app_name = 'vaga'

urlpatterns = [
    # URLs públicas
    path('', views.vaga_public, name='vaga_public'),
    path('<int:vaga_id>/', views.vaga_public_detail, name='vaga_public_detail'),
    
    # URLs de gerenciamento (requerem login)
    path('gerenciar/', views.vaga_list, name='vaga_list'),
    path('gerenciar/<int:vaga_id>/', views.vaga_detail, name='vaga_detail'),
    
    # Rota ÚNICA para iniciar o processo de adicionar vaga
    path('adicionar/', views.selecionar_instituicao_para_vaga, name='vaga_selecionar_instituicao'),
    
    # Rota que recebe o ID da instituição DEPOIS que o usuário a seleciona
    path('adicionar/<int:instituicao_id>/', views.vaga_create, name='vaga_create'),
    
    path('gerenciar/editar/<int:vaga_id>/', views.vaga_update, name='vaga_update'),
    path('gerenciar/apagar/<int:vaga_id>/', views.vaga_delete, name='vaga_delete'),
]
