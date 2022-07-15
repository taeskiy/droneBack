from rest_framework.permissions import BasePermission

from apps.user.models import User


class IsCrmAdmin(BasePermission):
    """
    Allows access only to CRM Admins.
    """

    def has_permission(self, request, view):
        return bool(request.user
                    and request.user.is_authenticated
                    and request.user.is_crm_admin)
