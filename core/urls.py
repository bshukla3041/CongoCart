from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('categories/', views.categories_view, name='categories'),
    path('sell/', views.product_add_view, name='sell'),
    path('buy/', views.categories_view, name='buy'),
    path('cart/', views.cart_view, name='cart'),
    path('shipping-address/', views.shipping_address_view, name='shipping-address'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('orders/', views.past_order_view, name='past-orders'),
    path('charge/', views.charge_view, name='charge'),
    path('<category>/', views.category_view, name='category_view'),
    path('<category>/<product_id>/', views.product_detail_view,
         name='product_detail_view'),
]
