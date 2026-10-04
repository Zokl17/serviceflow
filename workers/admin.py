from django import forms
from django.contrib import admin

from .models import Worker


WORKING_DAYS = [
    ("mon", "Пн"),
    ("tue", "Вт"),
    ("wed", "Ср"),
    ("thu", "Чт"),
    ("fri", "Пт"),
    ("sat", "Сб"),
    ("sun", "Вс"),
]


class WorkerAdminForm(forms.ModelForm):
    working_days = forms.MultipleChoiceField(
        label="Рабочие дни",
        choices=WORKING_DAYS,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Worker
        fields = "__all__"


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    form = WorkerAdminForm

    list_display = (
        "name",
        "phone",
        "is_available",
    )

    list_filter = (
        "is_available",
        "specializations",
    )

    search_fields = (
        "name",
        "phone",
    )

    filter_horizontal = (
        "specializations",
    )