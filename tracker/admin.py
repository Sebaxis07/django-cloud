from django.contrib import admin
from .models import Categoria, Transaccion

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo')
    list_filter = ('tipo',)
    search_fields = ('nombre',)

@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'descripcion', 'categoria', 'monto')
    list_filter = ('fecha', 'categoria', 'categoria__tipo')
    search_fields = ('descripcion', 'notas')
    date_hierarchy = 'fecha'
    list_editable = ('monto', 'categoria') # Cuidado con esto en producción
    ordering = ('-fecha',)