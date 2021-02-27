from django.db.models import signals
from django.dispatch import receiver

from orders import models


@receiver(signals.post_save, sender=models.Order)
def on_order_create_or_update(sender, **kwargs):
    """Updates product inventory when an order is created/updated.

    Updating an existing order should not impact the quantity, so same is
    ignored. For new orders, the quantity will be reduced accordingly.
    """
    order = kwargs["instance"]
    created = kwargs["created"]
    raw = kwargs["raw"]

    # Record inserted via fixture loading. Ignore
    if raw:
        return

    # Only discount is allowed to be updated in case any existing order is
    # edited, which shouldn't impact the product quantity.
    if not created:
        return

    order.product.quantity -= 1
    order.product.save()


@receiver(signals.post_delete, sender=models.Order)
def on_order_deleted(sender, **kwargs):
    """Updates the inventory when an existing order is deleted.

    Deleting an existing order presumeably results in product getting returned
    back to store, which should increase the product quantity.
    """
    order = kwargs["instance"]

    product = order.product
    product.quantity += 1
    product.save()
