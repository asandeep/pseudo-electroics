from django import forms
from django.core import exceptions

from orders import models


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ["product", "customer", "discount"]

    def clean_product(self):
        product = self.cleaned_data["product"]
        if not product.quantity:
            raise exceptions.ValidationError("This product is out of stock.")

        return product


class OrderUpdateForm(forms.ModelForm):
    read_only_fields = ["product", "customer"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.fields)
        for field in self.read_only_fields:
            widget = self.fields[field].widget
            widget.attrs["readonly"] = True

    class Meta:
        model = models.Order
        exclude = ["updated"]
