from decimal import Decimal, InvalidOperation

import cloudinary.uploader
from cloudinary.uploader import upload, destroy

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from users.permissions import IsManager
from .models import Vehicle, VehicleImage,Testimonial,VehicleDelivery

from .serializers import (
    VehicleImageCreateSerializer,
    VehicleImageSerializer,
    VehicleSerializer,
    TestimonialSerializer,
    VehicleDeliverySerializer,
)


# ==========================================================
# PUBLIC VEHICLE LIST
# ==========================================================

class VehicleListView(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request):

        # Customers can see only available vehicles.
        vehicles = Vehicle.objects.filter(
            is_available=True
        )

        # --------------------------------------------------
        # Search
        # --------------------------------------------------

        search = request.query_params.get("search")

        if search:
            vehicles = (
                vehicles.filter(
                    name__icontains=search
                )
                | vehicles.filter(
                    brand__icontains=search
                )
                | vehicles.filter(
                    model__icontains=search
                )
            )

        # --------------------------------------------------
        # Brand
        # --------------------------------------------------

        brand = request.query_params.get("brand")

        if brand:
            vehicles = vehicles.filter(
                brand__iexact=brand
            )

        # --------------------------------------------------
        # Vehicle Type
        # --------------------------------------------------

        vehicle_type = request.query_params.get(
            "vehicle_type"
        )

        if vehicle_type:
            vehicles = vehicles.filter(
                vehicle_type=vehicle_type.upper()
            )

        # --------------------------------------------------
        # Minimum Price
        # --------------------------------------------------

        min_price = request.query_params.get(
            "min_price"
        )

        if min_price:
            try:
                min_price = Decimal(min_price)

                vehicles = vehicles.filter(
                    price__gte=min_price
                )

            except InvalidOperation:
                return Response(
                    {
                        "success": False,
                        "message": "Invalid min_price.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # --------------------------------------------------
        # Maximum Price
        # --------------------------------------------------

        max_price = request.query_params.get(
            "max_price"
        )

        if max_price:
            try:
                max_price = Decimal(max_price)

                vehicles = vehicles.filter(
                    price__lte=max_price
                )

            except InvalidOperation:
                return Response(
                    {
                        "success": False,
                        "message": "Invalid max_price.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = VehicleSerializer(
            vehicles,
            many=True
        )

        return Response(
            {
                "success": True,
                "message": "Vehicles fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# MANAGER VEHICLE LIST
# ==========================================================

class ManagerVehicleListView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsManager,
    ]

    def get(self, request):

        # Managers can see ALL vehicles,
        # including unavailable vehicles.
        vehicles = Vehicle.objects.all()

        # --------------------------------------------------
        # Search
        # --------------------------------------------------

        search = request.query_params.get("search")

        if search:
            vehicles = (
                vehicles.filter(
                    name__icontains=search
                )
                | vehicles.filter(
                    brand__icontains=search
                )
                | vehicles.filter(
                    model__icontains=search
                )
            )

        # --------------------------------------------------
        # Brand
        # --------------------------------------------------

        brand = request.query_params.get("brand")

        if brand:
            vehicles = vehicles.filter(
                brand__iexact=brand
            )

        # --------------------------------------------------
        # Vehicle Type
        # --------------------------------------------------

        vehicle_type = request.query_params.get(
            "vehicle_type"
        )

        if vehicle_type:
            vehicles = vehicles.filter(
                vehicle_type=vehicle_type.upper()
            )

        # --------------------------------------------------
        # Availability
        # --------------------------------------------------

        is_available = request.query_params.get(
            "is_available"
        )

        if is_available is not None:

            if is_available.lower() == "true":
                vehicles = vehicles.filter(
                    is_available=True
                )

            elif is_available.lower() == "false":
                vehicles = vehicles.filter(
                    is_available=False
                )

        # --------------------------------------------------
        # Minimum Price
        # --------------------------------------------------

        min_price = request.query_params.get(
            "min_price"
        )

        if min_price:
            try:
                min_price = Decimal(min_price)

                vehicles = vehicles.filter(
                    price__gte=min_price
                )

            except InvalidOperation:
                return Response(
                    {
                        "success": False,
                        "message": "Invalid min_price.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # --------------------------------------------------
        # Maximum Price
        # --------------------------------------------------

        max_price = request.query_params.get(
            "max_price"
        )

        if max_price:
            try:
                max_price = Decimal(max_price)

                vehicles = vehicles.filter(
                    price__lte=max_price
                )

            except InvalidOperation:
                return Response(
                    {
                        "success": False,
                        "message": "Invalid max_price.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = VehicleSerializer(
            vehicles,
            many=True
        )

        return Response(
            {
                "success": True,
                "message": "Manager vehicles fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# MANAGER VEHICLE DETAIL
# ==========================================================

class ManagerVehicleDetailView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsManager,
    ]

    def get(
        self,
        request,
        vehicle_id
    ):

        try:

            # Manager can fetch an unavailable vehicle too.
            vehicle = Vehicle.objects.get(
                id=vehicle_id
            )

        except Vehicle.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Vehicle not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = VehicleSerializer(
            vehicle
        )

        return Response(
            {
                "success": True,
                "message": "Manager vehicle fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# PUBLIC VEHICLE DETAIL
# ==========================================================

class VehicleDetailView(APIView):

    authentication_classes = []
    permission_classes = []

    def get(
        self,
        request,
        vehicle_id
    ):

        try:

            # Public users can only access available vehicles.
            vehicle = Vehicle.objects.get(
                id=vehicle_id,
                is_available=True
            )

        except Vehicle.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Vehicle not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = VehicleSerializer(
            vehicle
        )

        return Response(
            {
                "success": True,
                "message": "Vehicle fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# CREATE VEHICLE
# ==========================================================

class VehicleCreateView(APIView):

    permission_classes = [
        IsManager
    ]

    def post(
        self,
        request
    ):

        serializer = VehicleSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        vehicle = serializer.save()

        return Response(
            {
                "success": True,
                "message": "Vehicle created successfully.",
                "data": VehicleSerializer(
                    vehicle
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


# ==========================================================
# UPDATE VEHICLE
# ==========================================================

class VehicleUpdateView(APIView):

    permission_classes = [
        IsManager
    ]

    def put(
        self,
        request,
        vehicle_id
    ):

        try:

            vehicle = Vehicle.objects.get(
                id=vehicle_id
            )

        except Vehicle.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Vehicle not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = VehicleSerializer(
            vehicle,
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        vehicle = serializer.save()

        return Response(
            {
                "success": True,
                "message": "Vehicle updated successfully.",
                "data": VehicleSerializer(
                    vehicle
                ).data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# DELETE VEHICLE
# ==========================================================

class VehicleDeleteView(APIView):

    permission_classes = [
        IsManager
    ]

    def delete(
        self,
        request,
        vehicle_id
    ):

        try:

            vehicle = Vehicle.objects.get(
                id=vehicle_id
            )

        except Vehicle.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Vehicle not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        vehicle.delete()

        return Response(
            {
                "success": True,
                "message": "Vehicle deleted successfully.",
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# CREATE VEHICLE IMAGE
# ==========================================================

class VehicleImageCreateView(APIView):

    permission_classes = [
        IsManager
    ]

    def post(
        self,
        request,
        vehicle_id
    ):

        try:

            vehicle = Vehicle.objects.get(
                id=vehicle_id
            )

        except Vehicle.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Vehicle not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = VehicleImageCreateSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        image = serializer.validated_data[
            "image"
        ]

        is_primary = serializer.validated_data.get(
            "is_primary",
            False
        )

        try:

            upload_result = (
                cloudinary.uploader.upload(
                    image,
                    folder=(
                        "anmol_automobile/"
                        f"vehicles/{vehicle.id}"
                    )
                )
            )

        except Exception:

            return Response(
                {
                    "success": False,
                    "message": "Image upload failed.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # If this image becomes primary,
        # remove primary status from other images.
        if is_primary:

            VehicleImage.objects.filter(
                vehicle=vehicle,
                is_primary=True
            ).update(
                is_primary=False
            )

        vehicle_image = (
            VehicleImage.objects.create(
                vehicle=vehicle,
                image_url=upload_result[
                    "secure_url"
                ],
                public_id=upload_result[
                    "public_id"
                ],
                is_primary=is_primary,
            )
        )

        return Response(
            {
                "success": True,
                "message": "Vehicle image uploaded successfully.",
                "data": VehicleImageSerializer(
                    vehicle_image
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


# ==========================================================
# DELETE VEHICLE IMAGE
# ==========================================================

class VehicleImageDeleteView(APIView):

    permission_classes = [
        IsManager
    ]

    def delete(
        self,
        request,
        vehicle_id,
        image_id
    ):

        try:

            vehicle = Vehicle.objects.get(
                id=vehicle_id
            )

        except Vehicle.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Vehicle not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        try:

            image = VehicleImage.objects.get(
                id=image_id,
                vehicle=vehicle
            )

        except VehicleImage.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Vehicle image not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        image.delete()

        return Response(
            {
                "success": True,
                "message": "Vehicle image deleted successfully.",
            },
            status=status.HTTP_200_OK,
        )

# ============================================================
# PUBLIC - TESTIMONIALS
# ============================================================


class PublicTestimonialListView(APIView):
    """
    Public endpoint.

    Returns the latest 6 published testimonials.
    """

    permission_classes = [
        # Public endpoint
    ]

    def get(self, request):

        testimonials = (
            Testimonial.objects
            .filter(is_published=True)
            .order_by("-created_at")[:6]
        )

        serializer = TestimonialSerializer(
            testimonials,
            many=True,
        )

        return Response(
            {
                "success": True,
                "message": "Testimonials fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# PUBLIC - SUBMIT TESTIMONIAL
# ============================================================


class SubmitTestimonialView(APIView):
    """
    Allows customers to submit testimonials.

    Submitted testimonials are unpublished by default
    and must be approved by a manager.
    """

    permission_classes = []

    def post(self, request):

        serializer = TestimonialSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "message": "Invalid testimonial data.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        testimonial = serializer.save(
            is_published=False,
            is_featured=False,
        )

        # ----------------------------------------------------
        # Optional customer image upload
        # ----------------------------------------------------

        image = request.FILES.get(
            "customer_image"
        )

        if image:

            try:

                result = upload(
                    image,
                    folder="anmol_automobile/testimonials",
                )

                testimonial.customer_image_url = (
                    result.get("secure_url", "")
                )

                testimonial.customer_image_public_id = (
                    result.get("public_id", "")
                )

                testimonial.save()

            except Exception as exc:

                return Response(
                    {
                        "success": False,
                        "message": (
                            "Testimonial was created, "
                            "but image upload failed."
                        ),
                        "error": str(exc),
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(
            {
                "success": True,
                "message": (
                    "Thank you for your feedback. "
                    "Your testimonial will be reviewed "
                    "before being published."
                ),
                "data": TestimonialSerializer(
                    testimonial
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


# ============================================================
# MANAGER - TESTIMONIALS
# ============================================================


class ManagerTestimonialListView(APIView):
    """
    Manager can see all testimonials including
    pending, published and featured testimonials.
    """

    permission_classes = [
        IsManager
    ]

    def get(self, request):

        testimonials = (
            Testimonial.objects
            .all()
            .order_by("-created_at")
        )

        serializer = TestimonialSerializer(
            testimonials,
            many=True,
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Manager testimonials "
                    "fetched successfully."
                ),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# MANAGER - APPROVE / FEATURE TESTIMONIAL
# ============================================================


class ApproveTestimonialView(APIView):
    """
    Manager approves a testimonial.

    Optional is_featured can also be supplied.
    """

    permission_classes = [
        IsManager
    ]

    def put(
        self,
        request,
        testimonial_id,
    ):

        try:

            testimonial = Testimonial.objects.get(
                id=testimonial_id
            )

        except Testimonial.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Testimonial not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        testimonial.is_published = True

        if "is_featured" in request.data:

            testimonial.is_featured = bool(
                request.data.get(
                    "is_featured"
                )
            )

        testimonial.save()

        return Response(
            {
                "success": True,
                "message": (
                    "Testimonial approved successfully."
                ),
                "data": TestimonialSerializer(
                    testimonial
                ).data,
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# MANAGER - UPDATE TESTIMONIAL
# ============================================================


class UpdateTestimonialView(APIView):
    """
    Manager can edit testimonial information
    and publication status.
    """

    permission_classes = [
        IsManager
    ]

    def put(
        self,
        request,
        testimonial_id,
    ):

        try:

            testimonial = Testimonial.objects.get(
                id=testimonial_id
            )

        except Testimonial.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Testimonial not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TestimonialSerializer(
            testimonial,
            data=request.data,
            partial=True,
        )

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "message": "Invalid testimonial data.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()

        # ----------------------------------------------------
        # Optional new customer image
        # ----------------------------------------------------

        image = request.FILES.get(
            "customer_image"
        )

        if image:

            try:

                # Delete old Cloudinary image
                if testimonial.customer_image_public_id:

                    try:

                        destroy(
                            testimonial.customer_image_public_id
                        )

                    except Exception:
                        pass

                # Upload new image
                result = upload(
                    image,
                    folder="anmol_automobile/testimonials",
                )

                testimonial.customer_image_url = (
                    result.get("secure_url", "")
                )

                testimonial.customer_image_public_id = (
                    result.get("public_id", "")
                )

                testimonial.save()

            except Exception as exc:

                return Response(
                    {
                        "success": False,
                        "message": (
                            "Testimonial updated, "
                            "but image upload failed."
                        ),
                        "error": str(exc),
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(
            {
                "success": True,
                "message": (
                    "Testimonial updated successfully."
                ),
                "data": TestimonialSerializer(
                    testimonial
                ).data,
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# MANAGER - DELETE TESTIMONIAL
# ============================================================


class DeleteTestimonialView(APIView):
    """
    Manager can permanently delete a testimonial.

    If the testimonial has a Cloudinary image,
    that image is also deleted.
    """

    permission_classes = [
        IsManager
    ]

    def delete(
        self,
        request,
        testimonial_id,
    ):

        try:

            testimonial = Testimonial.objects.get(
                id=testimonial_id
            )

        except Testimonial.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Testimonial not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # ----------------------------------------------------
        # Delete Cloudinary image
        # ----------------------------------------------------

        if testimonial.customer_image_public_id:

            try:

                destroy(
                    testimonial.customer_image_public_id
                )

            except Exception:

                # Don't block testimonial deletion
                # if Cloudinary deletion fails.
                pass

        testimonial.delete()

        return Response(
            {
                "success": True,
                "message": (
                    "Testimonial deleted successfully."
                ),
                "data": None,
            },
            status=status.HTTP_200_OK,
        )
# ============================================================
# PUBLIC - VEHICLE DELIVERIES
# ============================================================

class VehicleDeliveryListView(APIView):
    """
    Public endpoint for published vehicle deliveries.

    By default:
    - Returns all published deliveries.

    Optional:
    - ?limit=6
      Returns only the latest 6 published deliveries.
    """

    permission_classes = [AllowAny]

    def get(self, request):

        deliveries = (
            VehicleDelivery.objects
            .filter(
                is_published=True
            )
            .order_by(
                "-delivery_date",
                "-created_at",
            )
        )

        # ----------------------------------------------------
        # OPTIONAL LIMIT
        # ----------------------------------------------------

        limit = request.query_params.get(
            "limit"
        )

        if limit is not None:

            try:
                limit = int(limit)

                # Ignore invalid/non-positive values
                if limit > 0:
                    deliveries = deliveries[:limit]

            except (TypeError, ValueError):
                # If limit is invalid, simply return
                # all published deliveries.
                pass

        serializer = VehicleDeliverySerializer(
            deliveries,
            many=True,
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Published vehicle deliveries "
                    "fetched successfully."
                ),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

# ============================================================
# MANAGER - VEHICLE DELIVERIES
# ============================================================


class ManagerVehicleDeliveryListView(APIView):
    """
    Manager can see all deliveries.

    Includes:
    - Pending deliveries
    - Published deliveries
    """

    permission_classes = [IsManager]

    def get(self, request):

        deliveries = (
            VehicleDelivery.objects
            .all()
            .order_by(
                "-delivery_date",
                "-created_at",
            )
        )

        serializer = VehicleDeliverySerializer(
            deliveries,
            many=True,
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Manager deliveries "
                    "fetched successfully."
                ),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# MANAGER - CREATE DELIVERY
# ============================================================


class VehicleDeliveryCreateView(APIView):
    """
    Manager creates a vehicle delivery.

    The delivery image is uploaded to Cloudinary.
    New deliveries remain unpublished by default.
    """

    permission_classes = [IsManager]

    def post(self, request):

        serializer = VehicleDeliverySerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "message": "Validation failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        image = request.FILES.get("image")

        if not image:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Delivery image is required."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            upload_result = upload(
                image,
                folder="anmol_automobile/deliveries",
            )

        except Exception as exc:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Delivery image upload failed."
                    ),
                    "error": str(exc),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        delivery = serializer.save(
            image_url=upload_result.get(
                "secure_url",
                "",
            ),
            public_id=upload_result.get(
                "public_id",
                "",
            ),
            is_published=False,
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Vehicle delivery created "
                    "successfully. It is waiting "
                    "for publication."
                ),
                "data": VehicleDeliverySerializer(
                    delivery
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


# ============================================================
# MANAGER - PUBLISH DELIVERY
# ============================================================


class ApproveVehicleDeliveryView(APIView):
    """
    Manager publishes a vehicle delivery.
    """

    permission_classes = [IsManager]

    def put(
        self,
        request,
        delivery_id,
    ):

        try:
            delivery = VehicleDelivery.objects.get(
                id=delivery_id
            )

        except VehicleDelivery.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Vehicle delivery not found."
                    ),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        delivery.is_published = True
        delivery.save()

        return Response(
            {
                "success": True,
                "message": (
                    "Vehicle delivery published "
                    "successfully."
                ),
                "data": VehicleDeliverySerializer(
                    delivery
                ).data,
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# MANAGER - DELETE DELIVERY
# ============================================================


class DeleteVehicleDeliveryView(APIView):
    """
    Manager can permanently delete a delivery.

    The associated Cloudinary image is also deleted.
    """

    permission_classes = [IsManager]

    def delete(
        self,
        request,
        delivery_id,
    ):

        try:
            delivery = VehicleDelivery.objects.get(
                id=delivery_id
            )

        except VehicleDelivery.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Vehicle delivery not found."
                    ),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # ----------------------------------------------------
        # Delete Cloudinary image
        # ----------------------------------------------------

        if delivery.public_id:

            try:
                destroy(
                    delivery.public_id
                )

            except Exception:
                # Do not block database deletion
                # if Cloudinary deletion fails.
                pass

        delivery.delete()

        return Response(
            {
                "success": True,
                "message": (
                    "Vehicle delivery deleted "
                    "successfully."
                ),
                "data": None,
            },
            status=status.HTTP_200_OK,
        )