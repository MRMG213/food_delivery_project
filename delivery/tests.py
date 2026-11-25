from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Restaurant, Dish, Order, OrderItem

class DeliveryTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.restaurant = Restaurant.objects.create(name="Тестовый ресторан")
        self.dish = Dish.objects.create(name="Тестовое блюдо", restaurant=self.restaurant, price=500)
        self.order = Order.objects.create(title="Тестовый заказ", user=self.user, restaurant=self.restaurant)
        OrderItem.objects.create(order=self.order, dish=self.dish, quantity=2)

    def test_order_list_view(self):
        response = self.client.get(reverse("delivery:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тестовый заказ")

    def test_order_create_view(self):
        self.client.login(username="testuser", password="12345")
        data = {
            "title": "Новый заказ",
            "comment": "Комментарий",
            "restaurant": self.restaurant.pk,
            "is_paid": False,
            "order_items-TOTAL_FORMS": "1",
            "order_items-INITIAL_FORMS": "0",
            "order_items-MIN_NUM_FORMS": "0",
            "order_items-MAX_NUM_FORMS": "1000",
            "order_items-0-dish": self.dish.pk,
            "order_items-0-quantity": "2",
        }
        response = self.client.post(reverse("delivery:create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Order.objects.filter(title="Новый заказ").exists())

    def test_order_list_num_queries(self):
        with self.assertNumQueries(4):
            self.client.get(reverse("delivery:index"))