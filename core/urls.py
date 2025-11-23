from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('restaurants/', views.restaurant_list, name="restaurant_list"),
    path('restaurants/<int:pk>/', views.restaurant_detail, name="restaurant_detail"),
    path('cart/', views.view_cart, name="view_cart"),
    path('cart/add/<int:item_id>/', views.add_to_cart, name="add_to_cart"),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name="remove_from_cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('orders/', views.order_list, name="order_list"),
]
