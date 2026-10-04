from django import forms
from django.contrib import admin

from .models import Order, OrderStatusHistory


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["category"].empty_label = "Выберите категорию"
        self.fields["problem"].empty_label = "Выберите неисправность"

        if "assigned_worker" in self.fields:
            self.fields["assigned_worker"].empty_label = "Выберите мастера"


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory

    extra = 0
    can_delete = False

    fields = (
        "old_status_display",
        "new_status_display",
        "changed_by",
        "changed_at",
    )

    readonly_fields = (
        "old_status_display",
        "new_status_display",
        "changed_by",
        "changed_at",
    )

    @admin.display(description="Старый статус")
    def old_status_display(self, obj):
        if not obj.old_status:
            return "—"
        return obj.get_old_status_display()

    @admin.display(description="Новый статус")
    def new_status_display(self, obj):
        return obj.get_new_status_display()

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm

    inlines = (
        OrderStatusHistoryInline,
    )

    list_display = (
        "number",
        "customer_name",
        "phone",
        "category",
        "visit_date",
        "time_slot",
        "status",
        "assigned_worker",
        "created_at",
    )

    list_filter = (
        "status",
        "category",
        "assigned_worker",
        "visit_date",
    )

    search_fields = (
        "number",
        "customer_name",
        "phone",
        "street",
    )

    readonly_fields = (
        "number",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    def save_model(self, request, obj, form, change):
        old_status = None

        if change and obj.pk:
            old_status = (
                Order.objects
                .filter(pk=obj.pk)
                .values_list("status", flat=True)
                .first()
            )

        # Если назначили мастера, автоматически меняем статус.
        if (
            obj.assigned_worker_id
            and obj.status in (
                Order.Status.NEW,
                Order.Status.ACCEPTED,
            )
        ):
            obj.status = Order.Status.ASSIGNED

        super().save_model(request, obj, form, change)

        if not change:
            OrderStatusHistory.objects.create(
                order=obj,
                old_status="",
                new_status=obj.status,
                changed_by=request.user,
            )

        elif old_status != obj.status:
            OrderStatusHistory.objects.create(
                order=obj,
                old_status=old_status,
                new_status=obj.status,
                changed_by=request.user,
            )