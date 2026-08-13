from rest_framework import serializers
from .models import Vehicle, VehicleImage,VehicleDelivery,Testimonial


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


class ObjectIdRelatedField(serializers.PrimaryKeyRelatedField):
    """
    Handles MongoDB ObjectId primary keys.

    DRF's default PrimaryKeyRelatedField expects integer IDs,
    while Django MongoDB backend uses ObjectId.
    """

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except (TypeError, ValueError):
            raise serializers.ValidationError(
                "Invalid vehicle ID."
            )


class TestimonialSerializer(serializers.ModelSerializer):

    # MongoDB ObjectId -> string
    id = serializers.SerializerMethodField()

    vehicle = ObjectIdRelatedField(
        queryset=Vehicle.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Testimonial

        fields = [
            "id",
            "customer_name",
            "customer_location",
            "review",
            "rating",
            "customer_image_url",
            "customer_image_public_id",
            "vehicle",
            "is_published",
            "is_featured",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "customer_image_url",
            "customer_image_public_id",
            "is_published",
            "is_featured",
            "created_at",
            "updated_at",
        ]

    def get_id(self, obj):
        return str(obj.id)

    def validate_rating(self, value):

        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )

        return value

    def validate_customer_name(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Customer name is required."
            )

        return value

    def validate_review(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Review cannot be empty."
            )

        return value

class VehicleDeliverySerializer(serializers.ModelSerializer):

    # MongoDB ObjectId -> string
    id = serializers.SerializerMethodField()

    # MongoDB ObjectId vehicle relation -> string
    vehicle = ObjectIdRelatedField(
        queryset=Vehicle.objects.all(),
        required=False,
        allow_null=True,
    )

    vehicle_name = serializers.SerializerMethodField()

    vehicle_model = serializers.SerializerMethodField()

    class Meta:
        model = VehicleDelivery

        fields = [
            "id",
            "vehicle",
            "vehicle_name",
            "vehicle_model",
            "customer_name",
            "customer_location",
            "delivery_date",
            "image_url",
            "public_id",
            "caption",
            "is_published",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "image_url",
            "public_id",
            "vehicle_name",
            "vehicle_model",
            "is_published",
            "created_at",
            "updated_at",
        ]

    def get_id(self, obj):
        return str(obj.id)

    def get_vehicle_name(self, obj):
        if obj.vehicle:
            return obj.vehicle.name

        return None

    def get_vehicle_model(self, obj):
        if obj.vehicle:
            return obj.vehicle.model

        return None