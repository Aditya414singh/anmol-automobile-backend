from rest_framework import serializers

from .models import Vehicle, VehicleImage


class VehicleImageSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()

    class Meta:
        model = VehicleImage
        fields = [
            "id",
            "image_url",
            "public_id",
            "is_primary",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]

    def get_id(self, obj):
        return str(obj.id)


class VehicleSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()

    images = VehicleImageSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Vehicle
        fields = [
            "id",
            "name",
            "brand",
            "model",
            "vehicle_type",
            "price",
            "battery_capacity",
            "range_km",
            "charging_time",
            "seating_capacity",
            "payload_capacity",
            "top_speed",
            "description",
            "specifications",
            "is_available",
            "images",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "images",
            "created_at",
            "updated_at",
        ]

    def get_id(self, obj):
        return str(obj.id)


class VehicleImageCreateSerializer(serializers.Serializer):

    image = serializers.ImageField()

    is_primary = serializers.BooleanField(
        required=False,
        default=False,
    )