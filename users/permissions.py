from rest_framework.permissions import BasePermission

from .models import User


class IsCustomer(BasePermission):
    """
    Allows access only to authenticated customers.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Role.CUSTOMER
        )


class IsManager(BasePermission):
    """
    Allows access only to authenticated managers.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Role.MANAGER
        )


class IsCustomerOrManager(BasePermission):
    """
    Allows access to any authenticated user.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
        )