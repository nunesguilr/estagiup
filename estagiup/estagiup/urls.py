from django.contrib import admin
from django.urls import path, include
from . import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contas/', include('contas.urls')),
    path('cursos/', include('cursos.urls')),
    path('vagas/', include('vagas.urls')),
    path('estagios/', include('estagios.urls')),
    path('avaliacoes/', include('avaliacoes.urls')),
    path('notificacoes/', include('notificacoes.urls')),
    path('', views.index, name='home'),
]
