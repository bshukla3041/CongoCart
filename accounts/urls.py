from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('set-password/', views.password_set_view, name='set-password'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('update-profile/', views.update_profile_view, name='update-profile'),
]
