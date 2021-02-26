from datetime import datetime

from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=10)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Order(models.Model):
    discount = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=datetime.utcnow)
    updated = models.DateTimeField(auto_now=datetime.utcnow)

    # Foreign keys
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders"
    )
    product = models.ForeignKey(
        "inventory.Product", on_delete=models.CASCADE, related_name="orders"
    )

    class Meta:
        get_latest_by = "-created"
        ordering = ["-created"]

    def __str__(self):
        return f"{self.customer.name} - {self.product.name}"

    @property
    def price(self):
        if not self.discount:
            return self.product.price

        return self.product.price * ((100 - self.discount) / 100)
