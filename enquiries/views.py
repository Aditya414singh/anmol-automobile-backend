from datetime import timedelta

from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from users.permissions import IsManager
import logging

logger = logging.getLogger(__name__)

from .models import Enquiry
from .serializers import (
    EnquiryCreateSerializer,
    EnquiryManagerUpdateSerializer,
    EnquirySerializer,
)
from .services import send_enquiry_email


# ==========================================================
# PUBLIC - CREATE ENQUIRY
# ==========================================================


class EnquiryCreateView(APIView):
    """
    Public customer enquiry endpoint.

    Customer does not need to log in.

    Rate limits:
    - 5 requests per IP per hour
    - 3 enquiries per phone number per 24 hours
    """

    authentication_classes = []

    permission_classes = []

    throttle_classes = [
        AnonRateThrottle,
    ]

    def post(
        self,
        request,
    ):

        # --------------------------------------------------
        # VALIDATE REQUEST
        # --------------------------------------------------

        serializer = (
            EnquiryCreateSerializer(
                data=request.data
            )
        )

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "message": (
                        "Validation failed."
                    ),
                    "errors": (
                        serializer.errors
                    ),
                },
                status=(
                    status.HTTP_400_BAD_REQUEST
                ),
            )

        # --------------------------------------------------
        # PHONE RATE LIMIT
        # --------------------------------------------------

        phone = serializer.validated_data[
            "phone"
        ]

        twenty_four_hours_ago = (
            timezone.now()
            - timedelta(days=1)
        )

        recent_enquiries = (
            Enquiry.objects
            .filter(
                phone=phone,
                created_at__gte=(
                    twenty_four_hours_ago
                ),
            )
            .count()
        )

        if recent_enquiries >= 3:

            return Response(
                {
                    "success": False,
                    "message": (
                        "You have reached the "
                        "enquiry limit. Please "
                        "try again after some time."
                    ),
                    "code": (
                        "PHONE_RATE_LIMIT"
                    ),
                },
                status=(
                    status.HTTP_429_TOO_MANY_REQUESTS
                ),
            )

        # --------------------------------------------------
        # SAVE ENQUIRY
        # --------------------------------------------------

        enquiry = serializer.save()

        # --------------------------------------------------
        # SEND MANAGER EMAIL
        # --------------------------------------------------

        email_sent = False

        try:

            send_enquiry_email(
                enquiry
            )

            email_sent = True

        except Exception:

            logger.exception(
                "Failed to send enquiry email for enquiry %s",
                enquiry.id,
            )

        # --------------------------------------------------
        # RESPONSE
        # --------------------------------------------------

        return Response(
            {
                "success": True,
                "message": (
                    "Your enquiry has been "
                    "submitted successfully."
                ),
                "data": EnquirySerializer(
                    enquiry
                ).data,
                "notification_sent": (
                    email_sent
                ),
            },
            status=(
                status.HTTP_201_CREATED
            ),
        )


# ==========================================================
# MANAGER - LIST ENQUIRIES
# ==========================================================


class ManagerEnquiryListView(
    APIView
):
    """
    Manager can see all customer enquiries.
    """

    permission_classes = [
        IsAuthenticated,
        IsManager,
    ]

    def get(
        self,
        request,
    ):

        enquiries = (
            Enquiry.objects
            .all()
            .order_by(
                "-created_at"
            )
        )

        serializer = EnquirySerializer(
            enquiries,
            many=True,
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Customer enquiries "
                    "fetched successfully."
                ),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# MANAGER - UPDATE ENQUIRY
# ==========================================================


class ManagerEnquiryUpdateView(
    APIView
):
    """
    Manager can update enquiry status
    and internal notes.
    """

    permission_classes = [
        IsAuthenticated,
        IsManager,
    ]

    def patch(
        self,
        request,
        enquiry_id,
    ):

        try:

            enquiry = (
                Enquiry.objects.get(
                    id=enquiry_id
                )
            )

        except Enquiry.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Enquiry not found."
                    ),
                },
                status=(
                    status.HTTP_404_NOT_FOUND
                ),
            )

        serializer = (
            EnquiryManagerUpdateSerializer(
                enquiry,
                data=request.data,
                partial=True,
            )
        )

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "message": (
                        "Validation failed."
                    ),
                    "errors": (
                        serializer.errors
                    ),
                },
                status=(
                    status.HTTP_400_BAD_REQUEST
                ),
            )

        enquiry = serializer.save()

        return Response(
            {
                "success": True,
                "message": (
                    "Enquiry updated "
                    "successfully."
                ),
                "data": EnquirySerializer(
                    enquiry
                ).data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# MANAGER - DELETE ENQUIRY
# ==========================================================


class ManagerEnquiryDeleteView(
    APIView
):
    """
    Manager can delete an enquiry.
    """

    permission_classes = [
        IsAuthenticated,
        IsManager,
    ]

    def delete(
        self,
        request,
        enquiry_id,
    ):

        try:

            enquiry = (
                Enquiry.objects.get(
                    id=enquiry_id
                )
            )

        except Enquiry.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Enquiry not found."
                    ),
                },
                status=(
                    status.HTTP_404_NOT_FOUND
                ),
            )

        enquiry.delete()

        return Response(
            {
                "success": True,
                "message": (
                    "Enquiry deleted "
                    "successfully."
                ),
                "data": None,
            },
            status=status.HTTP_200_OK,
        )