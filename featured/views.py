from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from cloudinary.uploader import upload, destroy

from .models import FeaturedContent
from .serializers import FeaturedContentSerializer

from users.permissions import IsManager


# ============================================================
# PUBLIC - GET ACTIVE FEATURED CONTENT
# ============================================================

class FeaturedContentListView(APIView):
    """
    Public endpoint.

    Returns only featured content which:
    - is published
    - has started
    - has not expired

    The result is ordered by newest created content.
    """

    permission_classes = [AllowAny]

    def get(self, request):

        now = timezone.now()

        featured = (
            FeaturedContent.objects
            .filter(
                is_published=True,
                start_date__lte=now,
                end_date__gte=now,
            )
            .order_by("-created_at")
        )

        serializer = FeaturedContentSerializer(
            featured,
            many=True,
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Active featured content "
                    "fetched successfully."
                ),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# MANAGER - GET ALL FEATURED CONTENT
# ============================================================

class ManagerFeaturedContentListView(APIView):
    """
    Manager can see all featured content.

    Includes:
    - Draft/unpublished
    - Published
    - Scheduled
    - Expired
    """

    permission_classes = [IsManager]

    def get(self, request):

        featured = (
            FeaturedContent.objects
            .all()
            .order_by("-created_at")
        )

        serializer = FeaturedContentSerializer(
            featured,
            many=True,
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Manager featured content "
                    "fetched successfully."
                ),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# MANAGER - CREATE FEATURED CONTENT
# ============================================================

class FeaturedContentCreateView(APIView):
    """
    Manager creates featured content.

    The media file is uploaded to Cloudinary.

    Supported:
    - IMAGE
    - VIDEO

    New content remains unpublished by default.
    """

    permission_classes = [IsManager]

    def post(self, request):

        serializer = FeaturedContentSerializer(
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

        content_type = serializer.validated_data.get(
            "content_type"
        )

        media = request.FILES.get("media")

        if not media:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Featured media file is required."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ----------------------------------------------------
        # CLOUDINARY RESOURCE TYPE
        # ----------------------------------------------------

        resource_type = (
            "video"
            if content_type == "VIDEO"
            else "image"
        )

        # ----------------------------------------------------
        # UPLOAD
        # ----------------------------------------------------

        try:

            upload_result = upload(
                media,
                folder="anmol_automobile/featured",
                resource_type=resource_type,
            )

        except Exception as exc:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Featured media upload failed."
                    ),
                    "error": str(exc),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # ----------------------------------------------------
        # CREATE DATABASE RECORD
        # ----------------------------------------------------

        featured = serializer.save(
            media_url=upload_result.get(
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
                    "Featured content created "
                    "successfully. It is waiting "
                    "for publication."
                ),
                "data": FeaturedContentSerializer(
                    featured
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


# ============================================================
# MANAGER - UPDATE FEATURED CONTENT
# ============================================================

class FeaturedContentUpdateView(APIView):
    """
    Manager can update featured content.

    Media can optionally be replaced.
    """

    permission_classes = [IsManager]

    def put(
        self,
        request,
        featured_id,
    ):

        # ----------------------------------------------------
        # GET FEATURED CONTENT
        # ----------------------------------------------------

        try:

            featured = FeaturedContent.objects.get(
                id=featured_id
            )

        except FeaturedContent.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Featured content not found."
                    ),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # ----------------------------------------------------
        # SAVE OLD CLOUDINARY DETAILS
        # ----------------------------------------------------

        old_public_id = featured.public_id
        old_content_type = featured.content_type

        # ----------------------------------------------------
        # VALIDATE REQUEST DATA
        # ----------------------------------------------------

        serializer = FeaturedContentSerializer(
            featured,
            data=request.data,
            partial=True,
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

        # ----------------------------------------------------
        # CHECK FOR NEW MEDIA
        # ----------------------------------------------------

        media = request.FILES.get("media")

        if media:

            # Use the new content type if provided.
            # Otherwise keep the existing one.

            new_content_type = (
                serializer.validated_data.get(
                    "content_type",
                    featured.content_type,
                )
            )

            resource_type = (
                "video"
                if new_content_type == "VIDEO"
                else "image"
            )

            # ------------------------------------------------
            # UPLOAD NEW MEDIA
            # ------------------------------------------------

            try:

                upload_result = upload(
                    media,
                    folder="anmol_automobile/featured",
                    resource_type=resource_type,
                )

            except Exception as exc:

                return Response(
                    {
                        "success": False,
                        "message": (
                            "Featured media upload failed."
                        ),
                        "error": str(exc),
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # ------------------------------------------------
            # SAVE NEW MEDIA DETAILS
            # ------------------------------------------------

            featured = serializer.save(
                media_url=upload_result.get(
                    "secure_url",
                    "",
                ),
                public_id=upload_result.get(
                    "public_id",
                    "",
                ),
            )

            # ------------------------------------------------
            # DELETE OLD CLOUDINARY MEDIA
            # ------------------------------------------------

            if old_public_id:

                try:

                    destroy(
                        old_public_id,
                        resource_type=(
                            "video"
                            if old_content_type == "VIDEO"
                            else "image"
                        ),
                    )

                except Exception:
                    # Do not fail the database update
                    # if Cloudinary cleanup fails.
                    pass

        else:

            # ------------------------------------------------
            # UPDATE ONLY TEXT / DATE / OTHER FIELDS
            # ------------------------------------------------

            featured = serializer.save()

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return Response(
            {
                "success": True,
                "message": (
                    "Featured content updated "
                    "successfully."
                ),
                "data": FeaturedContentSerializer(
                    featured
                ).data,
            },
            status=status.HTTP_200_OK,
        )

# ============================================================
# MANAGER - PUBLISH FEATURED CONTENT
# ============================================================

class PublishFeaturedContentView(APIView):
    """
    Manager publishes featured content.

    Only one featured campaign is published at a time.
    Publishing a new one automatically unpublishes
    the previously published campaign.
    """

    permission_classes = [IsManager]

    def put(
        self,
        request,
        featured_id,
    ):

        try:

            featured = FeaturedContent.objects.get(
                id=featured_id
            )

        except FeaturedContent.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Featured content not found."
                    ),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # ----------------------------------------------------
        # UNPUBLISH OTHER CONTENT
        # ----------------------------------------------------

        (
            FeaturedContent.objects
            .filter(is_published=True)
            .exclude(id=featured.id)
            .update(is_published=False)
        )

        # ----------------------------------------------------
        # PUBLISH CURRENT CONTENT
        # ----------------------------------------------------

        featured.is_published = True
        featured.save()

        return Response(
            {
                "success": True,
                "message": (
                    "Featured content published "
                    "successfully."
                ),
                "data": FeaturedContentSerializer(
                    featured
                ).data,
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# MANAGER - UNPUBLISH FEATURED CONTENT
# ============================================================

class UnpublishFeaturedContentView(APIView):
    """
    Manager can manually unpublish featured content.
    """

    permission_classes = [IsManager]

    def put(
        self,
        request,
        featured_id,
    ):

        try:

            featured = FeaturedContent.objects.get(
                id=featured_id
            )

        except FeaturedContent.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Featured content not found."
                    ),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        featured.is_published = False
        featured.save()

        return Response(
            {
                "success": True,
                "message": (
                    "Featured content unpublished "
                    "successfully."
                ),
                "data": FeaturedContentSerializer(
                    featured
                ).data,
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# MANAGER - DELETE FEATURED CONTENT
# ============================================================

class DeleteFeaturedContentView(APIView):
    """
    Manager can permanently delete featured content.

    The associated Cloudinary media is also deleted.
    """

    permission_classes = [IsManager]

    def delete(
        self,
        request,
        featured_id,
    ):

        try:

            featured = FeaturedContent.objects.get(
                id=featured_id
            )

        except FeaturedContent.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Featured content not found."
                    ),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # ----------------------------------------------------
        # DELETE CLOUDINARY MEDIA
        # ----------------------------------------------------

        if featured.public_id:

            try:

                destroy(
                    featured.public_id,
                    resource_type=(
                        "video"
                        if featured.content_type == "VIDEO"
                        else "image"
                    ),
                )

            except Exception:
                # Database deletion should not fail
                # because of Cloudinary cleanup.
                pass

        # ----------------------------------------------------
        # DELETE DATABASE RECORD
        # ----------------------------------------------------

        featured.delete()

        return Response(
            {
                "success": True,
                "message": (
                    "Featured content deleted "
                    "successfully."
                ),
                "data": None,
            },
            status=status.HTTP_200_OK,
        )