from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Restaurant, MenuItem, Cart, CartItem, Order, OrderItem
from django.db import transaction

def home(request):
    return redirect("restaurant_list")

def restaurant_list(request):
    restaurants = Restaurant.objects.filter(is_active=True)
    return render(request, "core/restaurant_list.html", {"restaurants": restaurants})

def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk, is_active=True)
    categories = restaurant.categories.all()
    return render(request, "core/restaurant_detail.html", {"restaurant": restaurant, "categories": categories})

@login_required
def add_to_cart(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id, is_available=True)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect("view_cart")

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related("menu_item")
    total = sum(i.menu_item.price * i.quantity for i in items)
    return render(request, "core/cart.html", {"cart": cart, "items": items, "total": total})

@login_required
@transaction.atomic
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = list(cart.items.select_related("menu_item"))
    if not items:
        return redirect("restaurant_list")

    restaurant = items[0].menu_item.category.restaurant
    total = sum(i.menu_item.price * i.quantity for i in items)
    order = Order.objects.create(
        user=request.user,
        restaurant=restaurant,
        total_amount=total
    )
    for i in items:
        OrderItem.objects.create(
            order=order,
            menu_item=i.menu_item,
            price=i.menu_item.price,
            quantity=i.quantity,
        )
    cart.items.all().delete()
    return redirect("order_list")

@login_required
def order_list(request):
    orders = request.user.orders.select_related("restaurant").order_by("-created_at")
    return render(request, "core/order_list.html", {"orders": orders})
