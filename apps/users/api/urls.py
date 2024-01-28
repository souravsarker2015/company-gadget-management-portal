from django.urls import path
from apps.users.api import views

urlpatterns = [
    path('token2/', views.CustomTokenView.as_view(), name='token2'),
    path('user/register/', views.RegistrationView.as_view(), name='register'),
    path('user/login/', views.CustomLoginView.as_view(), name='custom-login'),
    path('user/logout/', views.CustomLogoutView.as_view(), name='custom-logout'),
]
