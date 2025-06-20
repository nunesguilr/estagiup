from django.urls import path
from . import views

urlpatterns = [
    path('', views.vaga_list, name='vaga_list'),
    path('<int:pk>/', views.vaga_detail, name='vaga_detail'),
    path('novo/', views.vaga_create, name='vaga_create'),
    path('<int:pk>/editar/', views.vaga_update, name='vaga_update'),
    path('<int:pk>/excluir/', views.vaga_delete, name='vaga_delete'),
    path('<int:pk>/candidatar/', views.vaga_apply, name='vaga_apply'),
]
