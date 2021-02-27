from datetime import datetime

from django.core import validators
from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(
        max_length=10, validators=[validators.RegexValidator(regex="\d{10}")]
    )
    email = models.EmailField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    discount = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Discount percentage",
        validators=[validators.MaxValueValidator(limit_value=100)],
    )
    created = models.DateTimeField(auto_now_add=datetime.utcnow)
    updated = models.DateTimeField(auto_now=datetime.utcnow)

    # Foreign keys
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, related_name="orders", null=True
    )
    product = models.ForeignKey(
        "inventory.Product", on_delete=models.PROTECT, related_name="orders"
    )

    class Meta:
        get_latest_by = "created"
        ordering = ["-created"]

    def __str__(self):
        return f"{self.customer.name} - {self.product.name}"

    @property
    def price(self):
        if not self.discount:
            return self.product.price

        return self.product.price * ((100 - self.discount) / 100)
