from django.db import models
from django.utils import timezone
from django.conf import settings
from catalog.models import Category, Problem


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новая"
        ACCEPTED = "accepted", "Принята"
        ASSIGNED = "assigned", "Назначен мастер"
        ON_THE_WAY = "on_the_way", "Мастер выехал"
        COMPLETED = "completed", "Выполнена"
        CANCELED = "canceled", "Отменена"

    class TimeSlot(models.TextChoices):
        MORNING = "09_12", "09:00–12:00"
        DAY = "12_15", "12:00–15:00"
        AFTERNOON = "15_18", "15:00–18:00"
        EVENING = "18_21", "18:00–21:00"

    number = models.CharField(
        "Номер заявки",
        max_length=20,
        unique=True,
        editable=False,
        blank=True,
    )

    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.PROTECT,
        related_name="orders",
    )

    manufacturer = models.CharField(
        "Производитель",
        max_length=100,
        blank=True,
    )

    problem = models.ForeignKey(
        Problem,
        verbose_name="Неисправность",
        on_delete=models.PROTECT,
        related_name="orders",
        null=True,
        blank=True,
    )

    problem_text = models.CharField(
        "Описание проблемы",
        max_length=255,
        blank=True,
    )

    city = models.CharField("Город", max_length=100)
    street = models.CharField("Улица", max_length=150)
    house = models.CharField("Дом", max_length=30)

    apartment = models.CharField(
        "Квартира",
        max_length=30,
        blank=True,
    )

    address_comment = models.TextField(
        "Комментарий к адресу",
        blank=True,
    )

    visit_date = models.DateField(
        "Дата визита",
    )

    time_slot = models.CharField(
        "Временной интервал",
        max_length=20,
        choices=[
            ("", "Выберите временной интервал"),
            *TimeSlot.choices,
        ],
    )

    customer_name = models.CharField(
        "Имя клиента",
        max_length=100,
    )

    phone = models.CharField(
        "Телефон",
        max_length=30,
    )

    customer_comment = models.TextField(
        "Комментарий клиента",
        blank=True,
    )

    status = models.CharField(
        "Статус",
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )

    assigned_worker = models.ForeignKey(
        "workers.Worker",
        verbose_name="Назначенный мастер",
        on_delete=models.SET_NULL,
        related_name="orders",
        null=True,
        blank=True,
    )

    internal_comment = models.TextField(
        "Внутренний комментарий",
        blank=True,
    )

    created_at = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "Последнее изменение",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new and not self.number:
            today = timezone.localdate().strftime("%Y%m%d")
            self.number = f"SF-{today}-{self.pk:06d}"

            super().save(
                update_fields=["number"],
            )
class OrderStatusHistory(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name="Заявка",
        on_delete=models.CASCADE,
        related_name="status_history",
    )

    old_status = models.CharField(
        "Старый статус",
        max_length=20,
        choices=Order.Status.choices,
        blank=True,
    )

    new_status = models.CharField(
        "Новый статус",
        max_length=20,
        choices=Order.Status.choices,
    )

    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Кто изменил",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    changed_at = models.DateTimeField(
        "Время изменения",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Изменение статуса"
        verbose_name_plural = "История статусов"
        ordering = ["-changed_at"]

    def __str__(self):
        return f"{self.order.number}: {self.old_status} → {self.new_status}"