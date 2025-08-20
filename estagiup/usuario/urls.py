from django.urls import path
from . import views

app_name = 'usuario'

urlpatterns = [
    path('registrar/', views.registrar_usuario, name='registrar'),
    path('login/', views.login_usuario, name='login'),
    path('lista/', views.lista_usuarios, name='lista_usuarios'),
    path('<int:pk>/', views.user_detail, name='user_detail'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('apagar/<int:pk>/', views.apagar_usuario, name='apagar_usuario'),
]
