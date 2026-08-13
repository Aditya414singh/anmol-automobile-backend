from django.urls import path

from .views import (
    FeaturedContentListView,
    ManagerFeaturedContentListView,
    FeaturedContentCreateView,
    FeaturedContentUpdateView,
    PublishFeaturedContentView,
    UnpublishFeaturedContentView,
    DeleteFeaturedContentView,
)


urlpatterns = [

    # ========================================================
    # PUBLIC
    # ========================================================

    path(
        "",
        FeaturedContentListView.as_view(),
        name="featured-list",
    ),

    # ========================================================
    # MANAGER
    # ========================================================

    path(
        "manager/",
        ManagerFeaturedContentListView.as_view(),
        name="manager-featured-list",
    ),

    path(
        "create/",
        FeaturedContentCreateView.as_view(),
        name="featured-create",
    ),

    path(
        "<str:featured_id>/update/",
        FeaturedContentUpdateView.as_view(),
        name="featured-update",
    ),

    path(
        "<str:featured_id>/publish/",
        PublishFeaturedContentView.as_view(),
        name="featured-publish",
    ),

    path(
        "<str:featured_id>/unpublish/",
        UnpublishFeaturedContentView.as_view(),
        name="featured-unpublish",
    ),

    path(
        "<str:featured_id>/delete/",
        DeleteFeaturedContentView.as_view(),
        name="featured-delete",
    ),
]