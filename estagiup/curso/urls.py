from django.urls import path
from . import views

app_name = 'curso'

urlpatterns = [
    path('', views.curso_list, name='curso_list'),
    path('adicionar/', views.curso_create, name='curso_create'),
    path('<int:curso_id>/', views.curso_detail, name='curso_detail'),
    path('<int:curso_id>/editar/', views.curso_update, name='curso_update'),
    path('<int:curso_id>/apagar/', views.curso_delete, name='curso_delete'),
]
