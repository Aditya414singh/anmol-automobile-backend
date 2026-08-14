from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "api/v1/auth/",
        include("users.urls"),
    ),

    path(
        "api/v1/vehicles/",
        include("vehicles.urls"),
    ),
    path(
        "api/v1/testimonials/",
        include("vehicles.testimonial_urls"),
    ),
    path(
    "api/v1/featured/",
    include("featured.urls"),
    ),
    path(
    "api/v1/enquiries/",
    include("enquiries.urls"),
    ),
]