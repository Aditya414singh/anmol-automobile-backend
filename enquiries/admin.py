from django.contrib import admin

from .models import Enquiry


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):

    list_display = (
        "customer_name",
        "phone",
        "vehicle",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "customer_name",
        "phone",
        "vehicle",
        "message",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )