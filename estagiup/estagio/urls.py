from django.urls import path
from . import views

app_name = 'estagio'

urlpatterns = [
    path('', views.estagio_list, name='estagio_list'),
    path('adicionar/<int:vaga_id>/', views.estagio_create, name='estagio_create'),
    path('<int:estagio_id>/', views.estagio_detail, name='estagio_detail'),
    path('<int:estagio_id>/editar/', views.estagio_update, name='estagio_update'),
    path('<int:estagio_id>/apagar/', views.estagio_delete, name='estagio_delete'),
]
