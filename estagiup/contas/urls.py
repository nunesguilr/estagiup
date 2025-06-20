from django.urls import path
from . import views

urlpatterns = [
    path('usuarios/', views.usuario_list, name='usuario_list'),
    path('usuarios/<int:pk>/', views.usuario_detail, name='usuario_detail'),
    path('usuarios/novo/', views.usuario_create, name='usuario_create'),
    path('usuarios/<int:pk>/editar/', views.usuario_update, name='usuario_update'),
    path('usuarios/<int:pk>/excluir/', views.usuario_delete, name='usuario_delete'),

    path('alunos/', views.aluno_list, name='aluno_list'),
    path('alunos/<int:pk>/', views.aluno_detail, name='aluno_detail'),
    path('alunos/novo/', views.aluno_create, name='aluno_create'),
    path('alunos/<int:pk>/editar/', views.aluno_update, name='aluno_update'),
    path('alunos/<int:pk>/excluir/', views.aluno_delete, name='aluno_delete'),

    path('empresas/', views.empresa_list, name='empresa_list'),
    path('empresas/<int:pk>/', views.empresa_detail, name='empresa_detail'),
    path('empresas/novo/', views.empresa_create, name='empresa_create'),
    path('empresas/<int:pk>/editar/', views.empresa_update, name='empresa_update'),
    path('empresas/<int:pk>/excluir/', views.empresa_delete, name='empresa_delete'),

    path('supervisores/', views.supervisor_list, name='supervisor_list'),
    path('supervisores/<int:pk>/', views.supervisor_detail, name='supervisor_detail'),
    path('supervisores/novo/', views.supervisor_create, name='supervisor_create'),
    path('supervisores/<int:pk>/editar/', views.supervisor_update, name='supervisor_update'),
    path('supervisores/<int:pk>/excluir/', views.supervisor_delete, name='supervisor_delete'),

    path('professores/', views.professor_list, name='professor_list'),
    path('professores/<int:pk>/', views.professor_detail, name='professor_detail'),
    path('professores/novo/', views.professor_create, name='professor_create'),
    path('professores/<int:pk>/editar/', views.professor_update, name='professor_update'),
    path('professores/<int:pk>/excluir/', views.professor_delete, name='professor_delete'),

    path('instituicoes/', views.instituicao_list, name='instituicao_list'),
    path('instituicoes/<int:pk>/', views.instituicao_detail, name='instituicao_detail'),
    path('instituicoes/novo/', views.instituicao_create, name='instituicao_create'),
    path('instituicoes/<int:pk>/editar/', views.instituicao_update, name='instituicao_update'),
    path('instituicoes/<int:pk>/excluir/', views.instituicao_delete, name='instituicao_delete'),
]
