from django.urls import path
from . import views

urlpatterns = [
    path('', views.notificacao_list, name='notificacao_list'),
    path('<int:pk>/', views.notificacao_detail, name='notificacao_detail'),
    path('<int:pk>/marcar_lida/', views.notificacao_marcar_lida, name='notificacao_marcar_lida'),
]
