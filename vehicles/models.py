from django.db import models


class Vehicle(models.Model):

    VEHICLE_TYPES = [
        ("E_RICKSHAW", "E-Rickshaw"),
        ("CARGO", "Cargo E-Rickshaw"),
    ]

    name = models.CharField(max_length=150)

    brand = models.CharField(max_length=100)

    model = models.CharField(max_length=100)

    vehicle_type = models.CharField(
        max_length=30,
        choices=VEHICLE_TYPES,
        default="E_RICKSHAW",
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    battery_capacity = models.CharField(
        max_length=50,
        blank=True,
    )

    range_km = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    charging_time = models.CharField(
        max_length=50,
        blank=True,
    )

    seating_capacity = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    payload_capacity = models.CharField(
        max_length=50,
        blank=True,
    )

    top_speed = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    specifications = models.JSONField(
        default=dict,
        blank=True,
    )

    is_available = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.brand} {self.model}"

class VehicleImage(models.Model):

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image_url = models.URLField()

    public_id = models.CharField(
        max_length=255,
        blank=True,
    )

    is_primary = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-is_primary", "created_at"]

    def __str__(self):
        return f"Image - {self.vehicle}"


class Testimonial(models.Model):

    customer_name = models.CharField(
        max_length=150,
    )

    customer_location = models.CharField(
        max_length=150,
        blank=True,
    )

    review = models.TextField()

    rating = models.PositiveSmallIntegerField(
        default=5,
    )

    customer_image_url = models.URLField(
        blank=True,
    )

    customer_image_public_id = models.CharField(
        max_length=255,
        blank=True,
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="testimonials",
    )

    is_published = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )
    is_featured = models.BooleanField(
    default=False,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer_name} - {self.rating}/5"


class VehicleDelivery(models.Model):

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deliveries",
    )

    customer_name = models.CharField(
        max_length=150,
        blank=True,
    )

    customer_location = models.CharField(
        max_length=150,
        blank=True,
    )

    delivery_date = models.DateField()

    image_url = models.URLField()

    public_id = models.CharField(
        max_length=255,
        blank=True,
    )

    caption = models.CharField(
        max_length=255,
        blank=True,
    )

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
            "-delivery_date",
            "-created_at",
        ]

    def __str__(self):
        return (
            f"{self.customer_name} - "
            f"{self.delivery_date}"
        )