from django.db import models
from django.conf import settings

class Restaurant(models.Model):
    name = models.CharField("Название ресторана", max_length=200, unique=True)
    
    def __str__(self):
        return self.name

class Dish(models.Model):
    name = models.CharField("Название блюда", max_length=200)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="dishes")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"

class Order(models.Model):
    title = models.CharField("Название заказа", max_length=255)
    comment = models.TextField("Комментарий к заказу", blank=True)
    is_paid = models.BooleanField("Оплачен", default=False)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Изменен", auto_now=True)
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="orders", verbose_name="Пользователь"
    )
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.SET_NULL, null=True,
        related_name="orders", verbose_name="Ресторан"
    )
    dishes = models.ManyToManyField(Dish, through="OrderItem", related_name="orders")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def total_price(self):
        # Специальный критерий 1: автоматический расчёт суммы
        return sum(item.get_total() for item in self.order_items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("Количество", default=1)

    def get_total(self):
        return self.dish.price * self.quantity