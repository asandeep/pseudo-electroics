import enum

from rolepermissions import roles


class Permission(enum.Enum):
    """Application specific permissions."""

    ACCOUNT__CREATE = "create_account"
    ACCOUNT__VIEW = "view_account"
    ACCOUNT__UPDATE = "update_account"
    ORDER__CREATE = "create_order"
    ORDER__VIEW = "view_order"
    ORDER__UPDATE = "update_order"
    ORDER__DELETE = "delete_order"
    CUSTOMER__VIEW = "view_customer_record"
    INVENTORY__VIEW = "view_inventory"
    INVENTORY_RECEIVING__VIEW = "view_inventory-receiving"
    INVENTORY_RECEIVING__CREATE = "create_inventory-receiving_record"


class StoreOwner(roles.AbstractUserRole):
    """Role that grants store owner access to user it is assigned to."""

    available_permissions = {
        permission.value: True for permission in Permission
    }


class StoreEmployee(roles.AbstractUserRole):
    """Role that grants employee access to user it is assigned to.

    An employee can access most of the views, and can create/update sales orders.
    """

    available_permissions = {
        Permission.ACCOUNT__VIEW.value: True,
        Permission.ACCOUNT__UPDATE.value: True,
        Permission.ORDER__VIEW.value: True,
        Permission.ORDER__CREATE.value: True,
        Permission.ORDER__UPDATE.value: True,
        Permission.CUSTOMER__VIEW.value: True,
        Permission.INVENTORY__VIEW.value: True,
        Permission.INVENTORY_RECEIVING__VIEW.value: True,
    }
