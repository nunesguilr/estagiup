from django.urls import path
from . import views

app_name = 'usuario'

urlpatterns = [
    path('registrar/', views.registrar_usuario, name='registrar'),
    path('login/', views.login_usuario, name='login'),
    path('lista/', views.lista_usuarios, name='lista_usuarios'),
    path('<int:user_id>/', views.user_detail_view, name='user_detail'),
]
