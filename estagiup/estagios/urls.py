from django.urls import path
from . import views

urlpatterns = [
    path('', views.estagio_list, name='estagio_list'),
    path('<int:pk>/', views.estagio_detail, name='estagio_detail'),
    path('novo/', views.estagio_create, name='estagio_create'),
    path('<int:pk>/editar/', views.estagio_update, name='estagio_update'),
    path('<int:pk>/excluir/', views.estagio_delete, name='estagio_delete'),
    path('<int:pk>/concluir/', views.estagio_concluir, name='estagio_concluir'),
    path('<int:pk>/cancelar/', views.estagio_cancelar, name='estagio_cancelar'),
]
