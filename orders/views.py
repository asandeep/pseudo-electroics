from django.contrib.messages import views as message_views
from django.urls import reverse_lazy
from django.views import generic as generic_views

from orders import forms, models


class OrderCreate(
    message_views.SuccessMessageMixin, generic_views.edit.CreateView
):
    model = models.Order
    form_class = forms.OrderForm
    template_name = "orders/orders-add.html"
    success_url = reverse_lazy("order-list")
    success_message = "Order successfully created."


class OrderDelete(
    message_views.SuccessMessageMixin, generic_views.edit.DeleteView
):
    model = models.Order
    success_url = reverse_lazy("order-list")
    template_name = "orders/orders-delete.html"
    success_message = "Order deleted."


class OrderUpdate(
    message_views.SuccessMessageMixin, generic_views.edit.UpdateView
):
    form_class = forms.OrderUpdateForm
    model = models.Order
    success_message = "Order updated."
    success_url = reverse_lazy("order-list")
    template_name = "orders/orders-update.html"
