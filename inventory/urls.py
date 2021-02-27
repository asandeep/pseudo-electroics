from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.views import generic as generic_views

from inventory import models, views

app_name = "inventory"

urlpatterns = [
    path("list/", login_required(views.ListInventory.as_view()), name="list"),
    path(
        "receiving/list/",
        login_required(views.ListInventoryReceiving.as_view()),
        name="list-receiving",
    ),
    path(
        "receiving/create/",
        login_required(views.CreateInventoryReceiving.as_view()),
        name="create-receiving",
    ),
]
