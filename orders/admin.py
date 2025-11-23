from django.contrib import admin
from .models import Restaurant, MenuCategory, MenuItem, Cart, CartItem, Order, OrderItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_veg", "food_type", "is_available")
    list_filter = ("is_veg", "food_type", "category", "is_available")
