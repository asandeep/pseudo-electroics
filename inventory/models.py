from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    quantity = models.PositiveSmallIntegerField()

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
    number = models.CharField(max_length=10)

    # Foreign keys
    distributor = models.ForeignKey(
        Distributor, on_delete=models.CASCADE, related_name="contacts"
    )

    def __str__(self):
        return f"{self.name} ({self.distributor.name})"


class InventoryReceived(models.Model):
    quantity = models.PositiveSmallIntegerField()
    distributor_price = models.PositiveSmallIntegerField()
    delivery_date = models.DateField()

    # Foreign keys
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="+"
    )
    distributor = models.ForeignKey(
        Distributor, on_delete=models.CASCADE, related_name="+"
    )

    def __str__(self):
        return f"{self.product.name} ({self.distributor.name}): {self.quantity}"
