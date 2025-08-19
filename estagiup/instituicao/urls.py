from django.urls import path
from . import views

app_name = 'instituicao'

urlpatterns = [
    path('cadastrar/', views.cadastrar_instituicao, name='cadastrar'),
    path('<int:instituicao_id>/membros/', views.listar_membros_instituicao, name='listar_membros'),
    path('<int:instituicao_id>/', views.perfil_instituicao, name='perfil'),
]
