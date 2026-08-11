from decimal import Decimal, InvalidOperation

import cloudinary.uploader

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsManager

from .models import Vehicle, VehicleImage
from .serializers import (
    VehicleImageCreateSerializer,
    VehicleImageSerializer,
    VehicleSerializer,
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