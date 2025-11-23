from django.urls import path
from . import views

urlpatterns = [
    path("", views.restaurant_list, name="restaurant_list"),
    path("restaurant/<int:pk>/", views.restaurant_detail, name="restaurant_detail"),

    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:item_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:item_id>/", views.update_cart_item, name="update_cart_item"),
    path("cart/remove/<int:item_id>/", views.remove_cart_item, name="remove_cart_item"),

    path("orders/", views.order_list, name="order_list"),

    path("signup/customer/", views.signup_customer, name="signup_customer"),
    path("signup/owner/", views.signup_owner, name="signup_owner"),
]
