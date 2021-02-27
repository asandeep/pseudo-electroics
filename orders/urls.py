from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.views import generic as generic_views

from orders import models, views

app_name = "orders"

urlpatterns = [
    path("list/", login_required(views.ListOrders.as_view()), name="list"),
    path("create/", login_required(views.CreateOrder.as_view()), name="create"),
    path(
        "update/<int:pk>/",
        login_required(views.UpdateOrder.as_view()),
        name="update",
    ),
    path(
        "delete/<int:pk>/",
        login_required(views.DeleteOrder.as_view()),
        name="delete",
    ),
    path(
        "customers/list/",
        login_required(views.ListCustomers.as_view()),
        name="list-customer",
    ),
]
