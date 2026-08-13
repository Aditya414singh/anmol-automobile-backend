from rest_framework import serializers

from .models import FeaturedContent


class FeaturedContentSerializer(
    serializers.ModelSerializer
):

    id = serializers.SerializerMethodField()

    class Meta:
        model = FeaturedContent

        fields = [
            "id",
            "title",
            "description",
            "content_type",
            "media_url",
            "public_id",
            "button_text",
            "button_url",
            "start_date",
            "end_date",
            "is_published",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "media_url",
            "public_id",
            "created_at",
            "updated_at",
        ]

    def get_id(self, obj):
        return str(obj.id)

    def validate_title(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Title is required."
            )

        return value

    def validate_end_date(self, value):

        start_date = self.initial_data.get(
            "start_date"
        )

        if start_date:

            try:
                start_date = serializers.DateTimeField().to_internal_value(
                    start_date
                )

                if value <= start_date:
                    raise serializers.ValidationError(
                        "End date must be after start date."
                    )

            except serializers.ValidationError:
                raise

        return value

    def validate_content_type(self, value):

        if value not in ["IMAGE", "VIDEO"]:
            raise serializers.ValidationError(
                "Content type must be IMAGE or VIDEO."
            )

        return value