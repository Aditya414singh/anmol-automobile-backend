from django.urls import path

from .views import (
    PublicTestimonialListView,
    SubmitTestimonialView,
    ManagerTestimonialListView,
    ApproveTestimonialView,
    UpdateTestimonialView,
    DeleteTestimonialView,
)


urlpatterns = [

    # ============================================================
    # PUBLIC
    # ============================================================

    path(
        "",
        PublicTestimonialListView.as_view(),
        name="public-testimonials",
    ),

    path(
        "submit/",
        SubmitTestimonialView.as_view(),
        name="submit-testimonial",
    ),

    # ============================================================
    # MANAGER
    # ============================================================

    path(
        "manager/",
        ManagerTestimonialListView.as_view(),
        name="manager-testimonials",
    ),

    path(
        "<str:testimonial_id>/approve/",
        ApproveTestimonialView.as_view(),
        name="approve-testimonial",
    ),

    path(
        "<str:testimonial_id>/update/",
        UpdateTestimonialView.as_view(),
        name="update-testimonial",
    ),

    path(
        "<str:testimonial_id>/delete/",
        DeleteTestimonialView.as_view(),
        name="delete-testimonial",
    ),
]