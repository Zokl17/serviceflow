from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Problem(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="problems",
    )

    name = models.CharField(
        max_length=150,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        verbose_name = "Неисправность"
        verbose_name_plural = "Неисправности"
        ordering = ["category", "name"]

        constraints = [
            models.UniqueConstraint(
                fields=["category", "name"],
                name="unique_problem_per_category",
            )
        ]

    def __str__(self):
        return f"{self.category}: {self.name}"