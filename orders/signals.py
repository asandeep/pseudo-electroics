from django.db.models import signals
from django.dispatch import receiver

from orders import models


@receiver(signals.post_save, sender=models.Order)
def on_new_order(sender, **kwargs):
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
    order = kwargs["instance"]

    product = order.product
    product.quantity += 1
    product.save()
