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

    VehicleDeliveryListView,
    ManagerVehicleDeliveryListView,
    VehicleDeliveryCreateView,
    ApproveVehicleDeliveryView,
    DeleteVehicleDeliveryView,
)


urlpatterns = [

    # ==========================================================
    # PUBLIC VEHICLES
    # ==========================================================

    path(
        "",
        VehicleListView.as_view(),
        name="vehicle-list",
    ),

    # ==========================================================
    # MANAGER VEHICLES
    # ==========================================================

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

    # ==========================================================
    # VEHICLE IMAGES
    # ==========================================================

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

    # ==========================================================
    # VEHICLE DELIVERIES
    # ==========================================================

    path(
        "deliveries/",
        VehicleDeliveryListView.as_view(),
        name="delivery-list",
    ),

    path(
        "deliveries/manager/",
        ManagerVehicleDeliveryListView.as_view(),
        name="manager-delivery-list",
    ),

    path(
        "deliveries/create/",
        VehicleDeliveryCreateView.as_view(),
        name="delivery-create",
    ),

    path(
        "deliveries/<str:delivery_id>/approve/",
        ApproveVehicleDeliveryView.as_view(),
        name="delivery-approve",
    ),

    path(
        "deliveries/<str:delivery_id>/delete/",
        DeleteVehicleDeliveryView.as_view(),
        name="delivery-delete",
    ),

    # ==========================================================
    # PUBLIC VEHICLE DETAIL
    # KEEP THIS LAST
    # ==========================================================

    path(
        "<str:vehicle_id>/",
        VehicleDetailView.as_view(),
        name="vehicle-detail",
    ),
]