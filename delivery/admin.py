from django.contrib import admin
from .models import Restaurant, Dish, Order, OrderItem

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "restaurant", "price")
    list_filter = ("restaurant",)
    search_fields = ("name",)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "restaurant", "is_paid", "created_at")
    list_filter = ("is_paid", "restaurant")
    search_fields = ("title", "comment")
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "dish", "quantity")