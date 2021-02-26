from django.db.models import signals
from django.dispatch import receiver

from inventory import models


@receiver(signals.post_save, sender=models.InventoryReceived)
def on_delivery_added(sender, **kwargs):
    inventory_received = kwargs["instance"]
    created = kwargs["created"]
    raw = kwargs["raw"]

    # Record inserted via fixture loading. Ignore
    if raw:
        return

    # A delivery record is not expected to be updated. Just in case it does,
    # ignore.
    if not created:
        return

    inventory_received.product.quantity += inventory_received.quantity
    inventory_received.product.save()
