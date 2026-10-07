from django.shortcuts import get_object_or_404, redirect, render

from .forms import OrderForm
from .models import Order


def home(request):
    return render(
        request,
        "orders/home.html",
    )


def create_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save()

            return redirect(
                "orders:success",
                number=order.number,
            )

    else:
        form = OrderForm()

    return render(
        request,
        "orders/order_form.html",
        {
            "form": form,
        },
    )


def order_success(request, number):
    order = get_object_or_404(
        Order,
        number=number,
    )

    return render(
        request,
        "orders/order_success.html",
        {
            "order": order,
        },
    )