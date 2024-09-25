from django.db import models


class NostroySmet(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Действует"),
        ("EXCLUDED", "Исключен"),
    ]

    id_number = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_inclusion_protocol = models.CharField(max_length=100, null=True, blank=True)
    type_of_work = models.TextField(null=True, blank=True)
    date_of_exclusion = models.CharField(max_length=100, null=True, blank=True)
    status_worker = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default="ACTIVE"
    )

    def __str__(self):
        return f"{self.id_number} {self.full_name}"

    class Meta:
        verbose_name = "Сметчик"
        verbose_name_plural = "Сметчики"
