from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem, Dish

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["title", "comment", "restaurant", "is_paid"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 3}),
        }

# Создаем formset: один заказ -> много позиций (OrderItem)
OrderItemFormSet = inlineformset_factory(
    Order, 
    OrderItem, 
    fields=("dish", "quantity"), 
    extra=3, # Показываем 3 пустые строки для добавления блюд
    can_delete=True
)