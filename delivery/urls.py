from django.urls import path
from . import views

app_name = "delivery"
urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.order_create, name="create"),
    path("<int:pk>/edit/", views.order_update, name="update"),
    path("<int:pk>/delete/", views.order_delete, name="delete"),
]