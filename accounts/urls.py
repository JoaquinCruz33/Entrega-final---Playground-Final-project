from django.urls import path
from django.contrib.auth import views as auth_views # Importamos las vistas de autenticación de Django
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logged_out.html'), name='logout'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/<int:pk>/edit/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
]