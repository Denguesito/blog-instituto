from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegistroUsuarioForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from .forms import PerfilUsuarioForm
from .models import Usuario

class RegistroUsuarioView(View):
    form_class = RegistroUsuarioForm
    template_name = 'usuarios/registro.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)  # loguea automáticamente al registrarse
            messages.success(request, f"Bienvenido {usuario.username}, tu cuenta fue creada correctamente.")
            return redirect('index.html')
        return render(request, self.template_name, {'form': form})


class LoginUsuarioView(View):
    template_name = 'usuarios/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            messages.success(request, f"Bienvenido {usuario.username}")
            return redirect('index.html')
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
            return render(request, self.template_name)

class PerfilUsuarioView(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = PerfilUsuarioForm
    template_name = 'usuarios/perfil.html'
    success_url = reverse_lazy('usuarios:perfil')

    def get_object(self, queryset=None):
        # Retorna el usuario logueado
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Perfil actualizado correctamente")
        return super().form_valid(form)

class LogoutUsuarioView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Has cerrado sesión correctamente")
        return redirect('index.html')

