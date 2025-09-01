from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Articulo, Categoria, ImagenArticulo
from .forms import ArticuloForm
from django.db.models import Sum
from apps.comentarios.models import Comentario
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class ArticuloListView(ListView):
    model = Articulo
    template_name = 'blog/lista_articulos.html'
    context_object_name = 'articulos'

    def get_queryset(self):
        queryset = super().get_queryset()
        categoria_id = self.request.GET.get('categoria')
        ordenar_por = self.request.GET.get('ordenar_por')

        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)

        if ordenar_por == 'asc':
            queryset = queryset.order_by('visitas')
        elif ordenar_por == 'desc':
            queryset = queryset.order_by('-visitas')
        elif ordenar_por == 'fecha_asc':
            queryset = queryset.order_by('fecha_publicacion')
        elif ordenar_por == 'fecha_desc':
            queryset = queryset.order_by('-fecha_publicacion')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context


class ArticuloDetailView(DetailView):
    model = Articulo
    template_name = 'blog/detalle_articulo.html'
    context_object_name = 'articulo'

    def get_object(self):
        articulo = super().get_object()
        articulo.visitas += 1
        articulo.save(update_fields=['visitas'])
        return articulo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comentarios'] = Comentario.objects.filter(articulo=self.object)
        return context

    def post(self, request, *args, **kwargs):
        articulo = self.get_object()
        contenido = request.POST.get('contenido')
        if contenido and request.user.is_authenticated:
            Comentario.objects.create(
                contenido=contenido,
                articulo=articulo,
                autor=request.user
            )
        return self.get(request, *args, **kwargs)


class ArticuloCreateView(LoginRequiredMixin, CreateView):
    model = Articulo
    form_class = ArticuloForm
    template_name = 'blog/crear_articulo.html'
    success_url = reverse_lazy('blog:lista_articulos')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        response = super().form_valid(form)
        # Guardar múltiples imágenes
        for archivo in self.request.FILES.getlist('imagenes'):
            ImagenArticulo.objects.create(articulo=self.object, imagen=archivo)
        return response


class ArticuloUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Articulo
    form_class = ArticuloForm
    template_name = 'blog/editar_articulo.html'
    success_url = reverse_lazy('blog:lista_articulos')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Agregar nuevas imágenes si el usuario sube más
        for archivo in self.request.FILES.getlist('imagenes'):
            ImagenArticulo.objects.create(articulo=self.object, imagen=archivo)
        return response

    def test_func(self):
        articulo = self.get_object()
        return (self.request.user == articulo.autor or
                self.request.user.is_superuser or
                self.request.user.is_staff)


class ArticuloDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Articulo
    template_name = 'blog/eliminar_articulo.html'
    success_url = reverse_lazy('blog:lista_articulos')

    def test_func(self):
        articulo = self.get_object()
        return (self.request.user == articulo.autor or
                self.request.user.is_superuser or
                self.request.user.is_staff)


class PaginaPrincipalView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_visitas = Articulo.objects.aggregate(total_visitas=Sum('visitas'))['total_visitas'] or 0
        context['total_visitas'] = total_visitas
        return context
