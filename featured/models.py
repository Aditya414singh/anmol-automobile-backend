from django.db import models
from django_mongodb_backend.fields import ObjectIdAutoField


class FeaturedContent(models.Model):

    id = ObjectIdAutoField(
        primary_key=True,
    )

    CONTENT_TYPES = [
        ("IMAGE", "Image"),
        ("VIDEO", "Video"),
    ]

    title = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    content_type = models.CharField(
        max_length=10,
        choices=CONTENT_TYPES,
        default="IMAGE",
    )

    media_url = models.URLField()

    public_id = models.CharField(
        max_length=255,
        blank=True,
    )

    button_text = models.CharField(
        max_length=100,
        blank=True,
    )

    button_url = models.CharField(
        max_length=500,
        blank=True,
    )

    start_date = models.DateTimeField()

    end_date = models.DateTimeField()

    is_published = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "-created_at",
        ]

    def __str__(self):
        return self.title