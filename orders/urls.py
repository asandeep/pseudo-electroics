from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from django.views import generic as generic_views

from orders import models, views

urlpatterns = [
    path(
        "list/",
        generic_views.ListView.as_view(
            model=models.Order,
            template_name="orders/order-list.html",
            context_object_name="orders",
        ),
        name="order-list",
    ),
    path("add/", views.OrderCreate.as_view(), name="order-add"),
    path("delete/<int:pk>/", views.OrderDelete.as_view(), name="order-delete"),
    path("update/<int:pk>/", views.OrderUpdate.as_view(), name="order-update"),
    path(
        "customers/list/",
        generic_views.ListView.as_view(
            model=models.Customer,
            template_name="orders/customer-list.html",
            context_object_name="customers",
        ),
        name="customer-list",
    ),
]
