import random
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from delivery.models import Restaurant, Dish, Order, OrderItem

class Command(BaseCommand):
    help = "Заполняет базу тестовыми заказами"

    def add_arguments(self, parser):
        parser.add_argument("--orders", type=int, default=100_000)

    @transaction.atomic
    def handle(self, *args, **options):
        fake = Faker("ru_RU")
        User = get_user_model()
        
        # 1. Создаем 20 пользователей
        users = [User.objects.get_or_create(username=f"client{i}")[0] for i in range(20)]
        self.stdout.write("Пользователи созданы.")

        # 2. Создаем 50 ресторанов
        Restaurant.objects.bulk_create(
            [Restaurant(name=f"Ресторан {i}") for i in range(50)], ignore_conflicts=True
        )
        restaurants = list(Restaurant.objects.all())
        self.stdout.write("Рестораны созданы.")

        # 3. Создаем 200 блюд
        Dish.objects.bulk_create(
            [Dish(
                name=fake.word().capitalize() + " " + fake.word(),
                restaurant=random.choice(restaurants),
                price=Decimal(random.randint(100, 2000))
            ) for _ in range(200)], ignore_conflicts=True
        )
        dishes = list(Dish.objects.all())
        self.stdout.write("Блюда созданы.")

        # 4. Создаем 100 000 заказов пачками
        total = options["orders"]
        batch = 5000
        
        for start in range(0, total, batch):
            size = min(batch, total - start)
            
            # Создаем заказы
            orders = Order.objects.bulk_create([
                Order(
                    title=f"Заказ № {start + i + 1}",
                    comment=fake.text(max_nb_chars=100),
                    is_paid=random.random() < 0.7,
                    user=random.choice(users),
                    restaurant=random.choice(restaurants),
                )
                for i in range(size)
            ])
            
            # Создаем позиции заказов (OrderItem) — по 1-4 блюда на заказ
            order_items = []
            for order in orders:
                num_dishes = random.randint(1, 4)
                for dish in random.sample(dishes, num_dishes):
                    order_items.append(
                        OrderItem(
                            order_id=order.pk,
                            dish_id=dish.pk,
                            quantity=random.randint(1, 3)
                        )
                    )
            
            OrderItem.objects.bulk_create(order_items)
            self.stdout.write(f"Создано {start + size} из {total} заказов")