from rolepermissions import roles


class StoreOwner(roles.AbstractUserRole):
    available_permissions = {}


class StoreEmployee(roles.AbstractUserRole):
    available_permissions = {}
