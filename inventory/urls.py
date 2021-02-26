from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from django.views import generic as generic_views

from inventory import models, views

urlpatterns = [
    path(
        "delivery/",
        generic_views.ListView.as_view(
            model=models.InventoryReceived,
            template_name="inventory/inventory-deliveries.html",
            context_object_name="deliveries",
        ),
        name="inventory-delivery",
    ),
    path(
        "delivery/add/",
        views.DeliveryCreate.as_view(),
        name="inventory-delivery-add",
    ),
    path(
        "list/",
        generic_views.ListView.as_view(
            model=models.Product,
            template_name="inventory/inventory-list.html",
            context_object_name="products",
        ),
        name="inventory-list",
    ),
]
