import re

from rest_framework import serializers

from .models import Enquiry


# ==========================================================
# PUBLIC - CREATE ENQUIRY
# ==========================================================

class EnquiryCreateSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Enquiry

        fields = [
            "customer_name",
            "phone",
            "vehicle",
            "message",
        ]

    def validate_customer_name(
        self,
        value,
    ):

        value = value.strip()

        if len(value) < 2:

            raise serializers.ValidationError(
                "Please enter a valid name."
            )

        return value

    def validate_phone(
        self,
        value,
    ):

        value = value.strip()

        if not re.fullmatch(
            r"[0-9]{10}",
            value,
        ):

            raise serializers.ValidationError(
                "Phone number must contain exactly 10 digits."
            )

        return value

    def validate_vehicle(
        self,
        value,
    ):

        return value.strip()

    def validate_message(
        self,
        value,
    ):

        value = value.strip()

        if len(value) < 5:

            raise serializers.ValidationError(
                "Please enter a meaningful message."
            )

        return value


# ==========================================================
# GENERAL ENQUIRY SERIALIZER
# ==========================================================

class EnquirySerializer(
    serializers.ModelSerializer
):

    # MongoDB ObjectId -> string
    id = serializers.CharField(
        read_only=True
    )

    class Meta:

        model = Enquiry

        fields = [
            "id",
            "customer_name",
            "phone",
            "vehicle",
            "message",
            "status",
            "manager_notes",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# ==========================================================
# MANAGER - UPDATE ENQUIRY
# ==========================================================

class EnquiryManagerUpdateSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Enquiry

        fields = [
            "status",
            "manager_notes",
        ]

    def validate_status(
        self,
        value,
    ):

        allowed_statuses = {
            Enquiry.Status.NEW,
            Enquiry.Status.CONTACTED,
            Enquiry.Status.CLOSED,
        }

        if value not in allowed_statuses:

            raise serializers.ValidationError(
                "Invalid enquiry status."
            )

        return value