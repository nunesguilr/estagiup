from django.urls import path
from . import views

app_name = 'vaga' 

urlpatterns = [
    path('', views.vaga_list, name='vaga_list'),

]