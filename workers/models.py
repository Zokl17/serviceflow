from django.db import models

from catalog.models import Category


class Worker(models.Model):
    name = models.CharField(
        "Имя",
        max_length=100,
    )

    phone = models.CharField(
        "Телефон",
        max_length=30,
    )

    specializations = models.ManyToManyField(
        Category,
        verbose_name="Специализации",
        related_name="workers",
        blank=True,
    )

    working_days = models.JSONField(
        "Рабочие дни",
        default=list,
        blank=True,
    )

    is_available = models.BooleanField(
        "Доступен",
        default=True,
    )

    created_at = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"
        ordering = ["name"]

    def __str__(self):
        return self.name