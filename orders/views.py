from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import (
    Restaurant,
    MenuCategory,
    MenuItem,
    Cart,
    CartItem,
    Order,
    OrderItem,
)


# ---------- RESTAURANTS ----------

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, "orders/restaurant_list.html", {"restaurants": restaurants})


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)

    show_veg = request.GET.get("veg") == "1"
    food_type = request.GET.get("type")

    categories = restaurant.categories.prefetch_related("items")

    if show_veg or food_type:
        for cat in categories:
            qs = cat.items.all()
            if show_veg:
                qs = qs.filter(is_veg=True)
            if food_type:
                qs = qs.filter(food_type=food_type)
            cat.filtered_items = qs
    else:
        for cat in categories:
            cat.filtered_items = cat.items.all()

    context = {
        "restaurant": restaurant,
        "categories": categories,
        "show_veg": show_veg,
        "food_type": food_type,
    }
    return render(request, "orders/restaurant_detail.html", context)


# ---------- CART ----------

@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    total = Decimal("0.00")
    for item in cart.items.select_related("menu_item"):
        total += item.menu_item.price * item.quantity

    return render(request, "orders/cart.html", {"cart": cart, "total": total})


@login_required
def add_to_cart(request, item_id):
    menu_item = get_object_or_404(MenuItem, pk=item_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        menu_item=menu_item,
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"Added {menu_item.name} to your cart.")
    return redirect("restaurant_detail", pk=menu_item.category.restaurant.pk)


@login_required
def update_cart_item(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, pk=item_id)

    try:
        qty = int(request.POST.get("quantity", 1))
    except ValueError:
        qty = 1

    if qty <= 0:
        cart_item.delete()
        messages.info(request, "Item removed from cart.")
    else:
        cart_item.quantity = qty
        cart_item.save()
        messages.success(request, "Cart updated.")

    return redirect("cart")


@login_required
def remove_cart_item(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, pk=item_id)
    cart_item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect("cart")


# ---------- ORDERS HISTORY ----------

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/order_list.html", {"orders": orders})


# ---------- SIMPLE SIGNUP PLACEHOLDERS ----------

def signup_customer(request):
    return HttpResponse("Customer signup placeholder")


def signup_owner(request):
    return HttpResponse("Owner signup placeholder")
