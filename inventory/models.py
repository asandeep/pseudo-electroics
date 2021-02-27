from datetime import datetime

from django.core import validators
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=100)
    price = models.PositiveIntegerField()

    # The quantity is managed inline with product and automatically updated when
    # new inventory is added and/or new orders are placed.
    # The other way would be to calculate this value live based on all
    # historical inventories and orders, which can be expensive. Also, retention
    # policy might result in old data being archived to cold storage, which will
    # require some sort of hacks to make that approach work.
    quantity = models.PositiveSmallIntegerField(
        editable=False,
        help_text="Latest available quantity of product in inventory.",
    )

    def __str__(self):
        return self.name


class Distributor(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name


class DistributorContact(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(
        max_length=10,
        verbose_name="Mobile Number",
        validators=[validators.RegexValidator(regex="\d{10}")],
        help_text="Distributor contact number.",
    )

    # Foreign keys
    distributor = models.ForeignKey(
        Distributor, on_delete=models.CASCADE, related_name="contacts"
    )

    def __str__(self):
        return f"{self.name} ({self.distributor.name})"


class InventoryReceived(models.Model):
    quantity = models.PositiveSmallIntegerField()
    distributor_price = models.PositiveSmallIntegerField()
    delivery_date = models.DateField(default=datetime.utcnow)

    # Foreign keys
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="+"
    )
    distributor = models.ForeignKey(
        Distributor, on_delete=models.PROTECT, related_name="+"
    )

    def __str__(self):
        return f"{self.product.name} ({self.distributor.name}): {self.quantity}"
