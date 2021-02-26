from django.contrib.messages import views as message_views
from django.urls import reverse_lazy
from django.views import generic as generic_views

from inventory import models


class DeliveryCreate(
    message_views.SuccessMessageMixin, generic_views.edit.CreateView
):
    model = models.InventoryReceived
    fields = [
        "product",
        "distributor",
        "quantity",
        "distributor_price",
        "delivery_date",
    ]
    template_name = "inventory/inventory-delivery-add.html"
    success_url = reverse_lazy("inventory-delivery")
    success_message = "Record successfully added."
