from django.contrib.messages import views as message_views
from django.urls import reverse_lazy
from django.views import generic as generic_views
from rolepermissions import mixins as rolepermissions_mixins

from accounts import roles
from orders import forms, models


class ListOrders(
    rolepermissions_mixins.HasPermissionsMixin, generic_views.ListView
):
    """A view that lists existing orders.

    User should have view order permission to be able to access this view.
    """

    context_object_name = "orders"
    model = models.Order
    required_permission = roles.Permission.ORDER__VIEW.value
    template_name = "orders/list.html"


class CreateOrder(
    rolepermissions_mixins.HasPermissionsMixin,
    message_views.SuccessMessageMixin,
    generic_views.edit.CreateView,
):
    """A view that renders form to add new order into system.

    User should have permission to create order to access this view.
    """

    model = models.Order
    form_class = forms.OrderCreateForm
    required_permission = roles.Permission.ORDER__CREATE.value
    success_url = reverse_lazy("orders:list")
    success_message = "Order successfully created."
    template_name = "orders/create.html"


class UpdateOrder(
    rolepermissions_mixins.HasPermissionsMixin,
    message_views.SuccessMessageMixin,
    generic_views.edit.UpdateView,
):
    """A view that allows employee to update an existing order.

    User is not allowed to update product or customer information while updating
    existing order.
    """

    form_class = forms.OrderUpdateForm
    model = models.Order
    required_permission = roles.Permission.ORDER__UPDATE.value
    success_message = "Order updated."
    success_url = reverse_lazy("orders:list")
    template_name = "orders/update.html"


class DeleteOrder(
    rolepermissions_mixins.HasRoleMixin,
    message_views.SuccessMessageMixin,
    generic_views.edit.DeleteView,
):
    """View that allows store owner to delete an existing owner from system."""

    model = models.Order
    success_url = reverse_lazy("orders:list")
    success_message = "Order deleted."
    template_name = "orders/delete.html"


class ListCustomers(
    rolepermissions_mixins.HasPermissionsMixin, generic_views.ListView
):
    """View that lists existing customers along with some order metadata."""

    context_object_name = "customers"
    model = models.Customer
    required_permission = roles.Permission.CUSTOMER__VIEW.value
    template_name = "orders/customers/list.html"
