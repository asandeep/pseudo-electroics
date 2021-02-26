from django.contrib import admin

from orders import models


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    pass
