from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView as DjangoPasswordChangeView # Para la vista de cambio de contraseña

from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile

# Vista para el registro de usuarios
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login') # Redirige a la página de login después del registro
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        # Crear un perfil para el nuevo usuario
        Profile.objects.create(user=self.object)
        messages.success(self.request, '¡Tu cuenta ha sido creada exitosamente! Por favor, inicia sesión.')
        return response

# Vista para ver el perfil del usuario
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'profile' # Nombre de la variable en el contexto

    def get_object(self):
        # Asegura que solo el usuario logueado pueda ver su propio perfil
        # O el perfil del usuario especificado por PK si está permitido
        return self.request.user.profile

# Vista para editar el perfil del usuario
class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_form.html'
    context_object_name = 'profile'

    def get_object(self):
        # Asegura que solo el usuario logueado pueda editar su propio perfil
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['u_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
            context['p_form'] = self.get_form() # ProfileUpdateForm
        else:
            context['u_form'] = UserUpdateForm(instance=self.request.user)
            context['p_form'] = self.get_form() # ProfileUpdateForm
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado exitosamente!')
            return redirect('profile_detail', pk=self.object.user.pk)
        else:
            messages.error(request, 'Hubo un error al actualizar tu perfil. Por favor, revisa los datos.')
            return self.render_to_response(self.get_context_data(u_form=u_form, p_form=p_form))

    def test_func(self):
        # Solo el propietario del perfil puede editarlo
        profile = self.get_object()
        return self.request.user == profile.user

    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'pk': self.request.user.pk})

# Vista para cambiar la contraseña
class PasswordChangeView(LoginRequiredMixin, DjangoPasswordChangeView):
    template_name = 'accounts/password_change_form.html'
    success_url = reverse_lazy('profile_detail') # Redirige al perfil después de cambiar la contraseña

    def get_success_url(self):
        messages.success(self.request, '¡Tu contraseña ha sido cambiada exitosamente!')
        return reverse_lazy('profile_detail', kwargs={'pk': self.request.user.pk})