# estagiup/estagiup/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from estagiup import views as estagiup_views 
from usuario import views as usuario_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/login/', auth_views.LoginView.as_view(template_name='usuario/login.html'), name='login'),
    path('usuarios/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('dashboard/', estagiup_views.dashboard_view, name='dashboard'),
    path('', estagiup_views.index, name='home'),
    path('sobre/', estagiup_views.sobre_view, name='sobre'),

    path('usuarios/', include('usuario.urls')),
    path('instituicao/', include('instituicao.urls')),
    path('vaga/', include('vaga.urls')),
    path('curso/', include('curso.urls')), 
    path('estagio/', include('estagio.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)