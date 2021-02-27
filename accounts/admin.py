import rolepermissions
from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from accounts import forms, models


class UserAdmin(
    auth_admin.UserAdmin, rolepermissions.admin.RolePermissionsUserAdminMixin
):
    form = forms.UserChangeForm
    add_form = forms.UserCreationForm


admin.site.register(models.User, UserAdmin)
