from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField # Importar RichTextField
from django.contrib.auth.models import User # Importar el modelo User

class Page(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    subtitle = models.CharField(max_length=200, verbose_name="Subtítulo", blank=True, null=True)
    content = RichTextField(verbose_name="Contenido") # Usamos RichTextField
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True, verbose_name="Imagen Principal")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor") # Enlaza a un usuario

    class Meta:
        ordering = ['-created_at'] # Ordenar por fecha de creación descendente

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('page_detail', kwargs={'pk': self.pk})