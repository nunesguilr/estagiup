from django.contrib import admin
from django.urls import path, include
from . import views 
from .views import index, dashboard_view 

urlpatterns = [
    path('admin/', admin.site.urls),   
    path('sobre/', views.sobre_view, name='sobre'),
    path('', views.index, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('usuarios/', include('usuario.urls')),
    path('vaga/', include('vaga.urls')),
    path('instituicao/', include('instituicao.urls')),
]
