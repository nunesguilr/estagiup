from django.urls import path
from . import views

urlpatterns = [
    path('notas/', views.nota_list, name='nota_list'),
    path('notas/<int:pk>/', views.nota_detail, name='nota_detail'),
    path('notas/novo/<int:estagio_pk>/', views.nota_create, name='nota_create'),
    path('notas/<int:pk>/editar/', views.nota_update, name='nota_update'),
    path('notas/<int:pk>/excluir/', views.nota_delete, name='nota_delete'),

    path('relatorios/', views.relatorio_list, name='relatorio_list'),
    path('relatorios/<int:pk>/', views.relatorio_detail, name='relatorio_detail'),
    path('relatorios/novo/<int:estagio_pk>/', views.relatorio_create, name='relatorio_create'),
    path('relatorios/<int:pk>/editar/', views.relatorio_update, name='relatorio_update'),
    path('relatorios/<int:pk>/excluir/', views.relatorio_delete, name='relatorio_delete'),
    
    path('relatorios/<int:pk>/salvar_rascunho/', views.relatorio_salvar_rascunho, name='relatorio_salvar_rascunho'),
    path('relatorios/<int:pk>/enviar/', views.relatorio_enviar, name='relatorio_enviar'),
    path('relatorios/<int:pk>/historico/', views.relatorio_historico, name='relatorio_historico'),
    path('relatorios/<int:pk>/avaliar/', views.relatorio_avaliar, name='relatorio_avaliar'),
]
