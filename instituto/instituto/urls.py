from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('contacto', views.Nosotros, name='contacto'),
    path('blog/', include(('apps.blog.urls', 'blog'), namespace='blog')),
    path('comentarios/', include(('apps.comentarios.urls', 'comentarios'), namespace='comentarios')),
    path('usuarios/', include(('apps.usuarios.urls', 'usuarios'), namespace='usuarios')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
