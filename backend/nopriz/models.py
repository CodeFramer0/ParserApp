from django.db import models


class NoprizFiz(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Действует"),
        ("EXCLUDED", "Исключен"),
    ]

    id_number_img = models.URLField(max_length=200)
    full_name_img = models.URLField(max_length=200)
    date_of_inclusion_protocol_img = models.URLField(
        max_length=200, null=True, blank=True
    )
    date_of_modification_img = models.URLField(max_length=200, null=True, blank=True)
    id_number = models.CharField(max_length=50)
    full_name = models.CharField(max_length=255)
    date_of_inclusion_protocol = models.CharField(max_length=50, null=True, blank=True)
    date_of_modification = models.CharField(max_length=50, null=True, blank=True)
    date_of_issue_certificate = models.CharField(max_length=50, null=True, blank=True)
    type_of_work = models.TextField(null=True, blank=True)
    date_of_exclusion = models.CharField(max_length=50, null=True, blank=True)
    status_worker = models.CharField(
        max_length=100, choices=STATUS_CHOICES, null=True, blank=True
    )
    verified_id_number = models.BooleanField(default=False)
    id_number_verification_attempts = models.PositiveSmallIntegerField(default=0)
    is_parsed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id_number} {self.full_name}"

    class Meta:
        verbose_name = "Физ-лицо"
        verbose_name_plural = "Физ-лица"
        unique_together = (
            "id_number_img",
            "full_name_img",
        )


class NoprizYr(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Является членом"),
        ("EXCLUDED", "Исключен"),
    ]

    id_number = models.CharField(max_length=50)
    name_cpo = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    name_of_the_member_cpo = models.TextField()
    inn = models.CharField(max_length=50)
    ogrn = models.CharField(max_length=50)
    date_of_termination = models.CharField(max_length=50, null=True, blank=True)
    date_of_registration = models.CharField(max_length=50, null=True, blank=True)
    director = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.id_number}"

    class Meta:
        verbose_name = "Юр-лицо"
        verbose_name_plural = "Юр-лица"
