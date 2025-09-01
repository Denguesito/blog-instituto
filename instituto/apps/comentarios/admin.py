from django.contrib import admin
from .models import Comentario

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('articulo', 'autor', 'contenido', 'fecha')
    list_filter = ('fecha', 'articulo')
    search_fields = ('autor__username', 'contenido')

admin.site.register(Comentario,ComentarioAdmin)