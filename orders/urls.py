from django.urls import path

from . import views


app_name = "orders"


urlpatterns = [
    path(
        "",
        views.home,
        name="home",
    ),

    path(
        "order/",
        views.create_order,
        name="create",
    ),

    path(
        "order/success/<str:number>/",
        views.order_success,
        name="success",
    ),
]