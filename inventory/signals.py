from django.db.models import signals
from django.dispatch import receiver

from inventory import models


@receiver(signals.post_save, sender=models.InventoryReceived)
def on_inventory_received(sender, **kwargs):
    """
    A signal receiver that updates the product quantity when new inventory is
    received.
    """
    inventory_received = kwargs["instance"]
    created = kwargs["created"]
    raw = kwargs["raw"]

    # Record inserted via fixture loading. Ignore
    if raw:
        return

    # A receiving record is not expected to be updated. Just in case it does,
    # ignore.
    if not created:
        return

    inventory_received.product.quantity += inventory_received.quantity
    inventory_received.product.save()
