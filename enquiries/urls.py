from django.urls import path

from .views import (
    EnquiryCreateView,
    ManagerEnquiryDeleteView,
    ManagerEnquiryListView,
    ManagerEnquiryUpdateView,
)


urlpatterns = [

    # Public
    path(
        "",
        EnquiryCreateView.as_view(),
        name="create-enquiry",
    ),

    # Manager
    path(
        "manager/",
        ManagerEnquiryListView.as_view(),
        name="manager-enquiries",
    ),

    path(
        "manager/<str:enquiry_id>/",
        ManagerEnquiryUpdateView.as_view(),
        name="manager-enquiry-update",
    ),

    path(
        "manager/<str:enquiry_id>/delete/",
        ManagerEnquiryDeleteView.as_view(),
        name="manager-enquiry-delete",
    ),
]