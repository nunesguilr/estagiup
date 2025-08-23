from django.urls import path
from . import views

app_name = 'instituicao'

urlpatterns = [
    path('cadastrar/', views.cadastrar_instituicao, name='cadastrar'),
    path('<int:instituicao_id>/membros/', views.listar_membros_instituicao, name='listar_membros'),
    path('minhas/', views.minhas_instituicoes, name='minhas_instituicoes'),
    path('<int:instituicao_id>/', views.perfil_instituicao, name='perfil_instituicao'),
    path('<int:instituicao_id>/editar/', views.editar_instituicao, name='editar_instituicao'),
    path('<int:instituicao_id>/apagar/', views.apagar_instituicao, name='apagar_instituicao'),
]