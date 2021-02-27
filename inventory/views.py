from django.contrib.messages import views as message_views
from django.urls import reverse_lazy
from django.views import generic as generic_views
from rolepermissions import mixins as rolepermissions_mixins

from accounts import roles
from inventory import models


class ListInventory(
    rolepermissions_mixins.HasPermissionsMixin, generic_views.ListView
):
    """A view that shows the current inventory of products.

    User should have view inventory permissions to access this view.
    """

    context_object_name = "products"
    model = models.Product
    required_permission = roles.Permission.INVENTORY__VIEW.value
    template_name = "inventory/list.html"


class ListInventoryReceiving(
    rolepermissions_mixins.HasPermissionsMixin, generic_views.ListView
):
    """A view that shows the inventory received from various distributors.

    User should have view inventory receiving permissions to access this view.
    """

    context_object_name = "receiving"
    model = models.InventoryReceived
    required_permission = roles.Permission.INVENTORY_RECEIVING__VIEW.value
    template_name = "inventory/receiving/list.html"


class CreateInventoryReceiving(
    rolepermissions_mixins.HasRoleMixin,
    message_views.SuccessMessageMixin,
    generic_views.edit.CreateView,
):
    """A view that allows store owner to create an entry for received entry."""

    allowed_roles = roles.StoreOwner
    fields = [
        "product",
        "distributor",
        "quantity",
        "distributor_price",
        "delivery_date",
    ]
    model = models.InventoryReceived
    template_name = "inventory/receiving/create.html"
    success_message = "Record successfully added."
    success_url = reverse_lazy("inventory:list-receiving")
