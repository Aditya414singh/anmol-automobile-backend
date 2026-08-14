from django.db import models

from django_mongodb_backend.fields import (
    ObjectIdAutoField,
)


class Enquiry(models.Model):

    class Status(models.TextChoices):
        NEW = "NEW", "New"
        CONTACTED = "CONTACTED", "Contacted"
        CLOSED = "CLOSED", "Closed"

    id = ObjectIdAutoField(
        primary_key=True
    )

    customer_name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=10
    )

    vehicle = models.CharField(
        max_length=150,
        blank=True,
        default="",
    )

    message = models.TextField(
        max_length=2000
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )

    manager_notes = models.TextField(
        max_length=2000,
        blank=True,
        default="",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "-created_at"
        ]

    def __str__(self):
        return (
            f"{self.customer_name} - "
            f"{self.phone}"
        )