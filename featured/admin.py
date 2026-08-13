from django.contrib import admin

from .models import FeaturedContent


@admin.register(FeaturedContent)
class FeaturedContentAdmin(admin.ModelAdmin):

    list_display = [
        "title",
        "content_type",
        "start_date",
        "end_date",
        "is_published",
        "created_at",
    ]

    list_filter = [
        "content_type",
        "is_published",
    ]

    search_fields = [
        "title",
        "description",
    ]

    ordering = [
        "-created_at",
    ]