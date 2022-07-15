from rest_framework.permissions import BasePermission


class CartPermission(BasePermission):
    def has_permission(self, request, view):
        imei = request.headers.get('imei', None)
        if request.user.is_anonymous:
            return bool(imei)
        return bool(request.user and request.user.is_authenticated and imei)
