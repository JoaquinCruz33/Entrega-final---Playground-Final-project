# blog/views.py

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Page
from .forms import PageForm

# Vista para listar todas las páginas
class PageListView(ListView):
    model = Page
    template_name = 'blog/page_list.html'
    context_object_name = 'pages'
    paginate_by = 10 # Opcional: paginación

    def get_queryset(self):
        queryset = super().get_queryset()
        # Puedes añadir lógica de búsqueda aquí si la necesitas más adelante
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context['pages'] and not self.request.GET.get('q'): # Si no hay páginas y no se usó el buscador
            context['no_pages_message'] = 'No hay páginas publicadas aún. ¡Sé el primero en crear una!'
        return context

# Vista para ver el detalle de una página
class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/page_detail.html'
    context_object_name = 'page'

# Vista para crear una nueva página (requiere login)
class PageCreateView(LoginRequiredMixin, CreateView):
    model = Page
    form_class = PageForm
    template_name = 'blog/page_form.html'
    success_url = reverse_lazy('page_list') # Redirige a la lista después de crear

    def form_valid(self, form):
        form.instance.author = self.request.user # Asigna el autor actual
        messages.success(self.request, '¡La página ha sido creada exitosamente!')
        return super().form_valid(form)

# Vista para editar una página existente (requiere login y ser el autor)
class PageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Page
    form_class = PageForm
    template_name = 'blog/page_form.html'
    context_object_name = 'page'

    def get_success_url(self):
        messages.success(self.request, '¡La página ha sido actualizada exitosamente!')
        return reverse_lazy('page_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        # Solo el autor de la página o un superusuario puede editarla
        page = self.get_object()
        return self.request.user == page.author or self.request.user.is_superuser

# Vista para eliminar una página (requiere login y ser el autor)
class PageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Page
    template_name = 'blog/page_confirm_delete.html'
    success_url = reverse_lazy('page_list') # Redirige a la lista después de eliminar
    context_object_name = 'page'

    def form_valid(self, form):
        messages.success(self.request, '¡La página ha sido eliminada exitosamente!')
        return super().form_valid(form)

    def test_func(self):
        # Solo el autor de la página o un superusuario puede eliminarla
        page = self.get_object()
        return self.request.user == page.author or self.request.user.is_superuser