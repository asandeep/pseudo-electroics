from django import forms
from django.core import exceptions

from orders import models


class OrderCreateForm(forms.ModelForm):
    """Overrides base form to validate out of stock products."""

    class Meta:
        model = models.Order
        fields = ["product", "customer", "discount"]

    def clean_product(self):
        """
        Validates that the product being ordered is available in inventory.
        """
        product = self.cleaned_data["product"]
        if not product.quantity:
            raise exceptions.ValidationError("This product is out of stock.")

        return product


class OrderUpdateForm(forms.ModelForm):
    """
    Overrides base implementation to disable read only fields from getting
    updated.
    """

    # Fields that cannot be modifying while updating the order.
    _READ_ONLY_FIELDS = ["product", "customer"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self._READ_ONLY_FIELDS:
            widget = self.fields[field].widget
            widget.attrs["readonly"] = True

    class Meta:
        model = models.Order
        exclude = ["updated"]
