from django.urls import path
from . import views

urlpatterns = [
    path('', views.PageListView.as_view(), name='page_list'), # Ruta principal para la lista de páginas
    path('new/', views.PageCreateView.as_view(), name='page_create'),
    path('<int:pk>/', views.PageDetailView.as_view(), name='page_detail'),
    path('<int:pk>/edit/', views.PageUpdateView.as_view(), name='page_update'),
    path('<int:pk>/delete/', views.PageDeleteView.as_view(), name='page_delete'),
]