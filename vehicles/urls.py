from django.urls import path

from .views import (
    VehicleListView,
    ManagerVehicleListView,
    ManagerVehicleDetailView,
    VehicleDetailView,
    VehicleCreateView,
    VehicleUpdateView,
    VehicleDeleteView,
    VehicleImageCreateView,
    VehicleImageDeleteView,
)


urlpatterns = [

    path(
        "",
        VehicleListView.as_view(),
        name="vehicle-list",
    ),

    path(
        "manager/",
        ManagerVehicleListView.as_view(),
        name="manager-vehicle-list",
    ),

    path(
        "manager/<str:vehicle_id>/",
        ManagerVehicleDetailView.as_view(),
        name="manager-vehicle-detail",
    ),

    path(
        "create/",
        VehicleCreateView.as_view(),
        name="vehicle-create",
    ),

    path(
        "<str:vehicle_id>/images/",
        VehicleImageCreateView.as_view(),
        name="vehicle-image-create",
    ),

    path(
        "<str:vehicle_id>/images/<str:image_id>/",
        VehicleImageDeleteView.as_view(),
        name="vehicle-image-delete",
    ),

    path(
        "<str:vehicle_id>/update/",
        VehicleUpdateView.as_view(),
        name="vehicle-update",
    ),

    path(
        "<str:vehicle_id>/delete/",
        VehicleDeleteView.as_view(),
        name="vehicle-delete",
    ),

    # Keep public detail LAST
    path(
        "<str:vehicle_id>/",
        VehicleDetailView.as_view(),
        name="vehicle-detail",
    ),
]