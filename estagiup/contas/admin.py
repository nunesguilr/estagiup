from django.contrib import admin
from .models import Usuario, Aluno, ContaEmpresa, Supervisor, Professor, ContaInstituicao

admin.site.register(Usuario)
admin.site.register(Aluno)
admin.site.register(ContaEmpresa)
admin.site.register(Supervisor)
admin.site.register(Professor)
admin.site.register(ContaInstituicao)