from django import forms
from django.utils import timezone

from catalog.models import Category, Problem
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order

        fields = (
            "category",
            "manufacturer",
            "problem",
            "problem_text",
            "city",
            "street",
            "house",
            "apartment",
            "address_comment",
            "visit_date",
            "time_slot",
            "customer_name",
            "phone",
            "customer_comment",
        )

        widgets = {
            "visit_date": forms.DateInput(
                attrs={"type": "date"},
            ),
            "address_comment": forms.Textarea(
                attrs={"rows": 3},
            ),
            "customer_comment": forms.Textarea(
                attrs={"rows": 3},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["category"].queryset = Category.objects.filter(
            is_active=True
        )

        self.fields["problem"].queryset = Problem.objects.filter(
            is_active=True
        )

        self.fields["category"].empty_label = "Выберите категорию"
        self.fields["problem"].empty_label = "Выберите неисправность"

    def clean_visit_date(self):
        visit_date = self.cleaned_data["visit_date"]

        if visit_date < timezone.localdate():
            raise forms.ValidationError(
                "Нельзя выбрать прошедшую дату."
            )

        return visit_date

    def clean(self):
        cleaned_data = super().clean()

        category = cleaned_data.get("category")
        problem = cleaned_data.get("problem")

        if (
            category
            and problem
            and problem.category_id != category.id
        ):
            self.add_error(
                "problem",
                "Эта неисправность не относится к выбранной категории.",
            )

        return cleaned_data