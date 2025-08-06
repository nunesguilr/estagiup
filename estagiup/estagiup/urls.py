from django.contrib import admin
from django.urls import path, include
from . import views 
from .views import index, dashboard_view 

urlpatterns = [
    path('admin/', admin.site.urls),   
    path('', views.index, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
