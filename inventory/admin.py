from django.contrib import admin

from inventory import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Distributor)
class DistributorAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DistributorContact)
class DistributorContactAdmin(admin.ModelAdmin):
    pass


@admin.register(models.InventoryReceived)
class InventoryReceivedAdmin(admin.ModelAdmin):
    pass
