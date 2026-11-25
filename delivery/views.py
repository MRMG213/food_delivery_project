from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import Order, Restaurant, Dish, OrderItem
from .forms import OrderForm, OrderItemFormSet
from django.db.models import Prefetch

def index(request):
    orders = Order.objects.select_related("restaurant", "user").prefetch_related(
    Prefetch("order_items", queryset=OrderItem.objects.select_related("dish"))
)
    
    # Фильтры и поиск
    restaurant_id = request.GET.get("restaurant")
    if restaurant_id:
        orders = orders.filter(restaurant_id=restaurant_id)
        
    is_paid = request.GET.get("is_paid")
    if is_paid == "1":
        orders = orders.filter(is_paid=True)
    elif is_paid == "0":
        orders = orders.filter(is_paid=False)
        
    q = request.GET.get("q")
    if q:
        orders = orders.filter(Q(title__icontains=q) | Q(comment__icontains=q))
        
    # Пагинация
    paginator = Paginator(orders, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    restaurants = Restaurant.objects.all()
    
    return render(request, "delivery/order_list.html", {
        "page_obj": page_obj,
        "restaurants": restaurants,
    })

def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            order = form.save(commit=False)
            order.user = request.user # Привязываем к текущему пользователю
            order.save()
            formset.instance = order
            formset.save()
            return redirect("delivery:index")
    else:
        form = OrderForm()
        formset = OrderItemFormSet()
    
    return render(request, "delivery/order_form.html", {
        "form": form, 
        "formset": formset, 
        "title": "Новый заказ"
    })

def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("delivery:index")
    else:
        form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)
    
    return render(request, "delivery/order_form.html", {
        "form": form, 
        "formset": formset, 
        "title": "Редактирование заказа"
    })

def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order.delete()
        return redirect("delivery:index")
    return render(request, "delivery/order_confirm_delete.html", {"order": order})