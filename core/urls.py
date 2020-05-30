from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('sell/', views.product_add_view, name='sell'),
    path('buy/', views.home_view, name='buy'),
    path('<category>/', views.category_view, name='category_view'),
]