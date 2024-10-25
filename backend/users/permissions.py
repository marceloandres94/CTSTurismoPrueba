from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):
    """
    Permiso personalizado para restringir el acceso solo a superusuarios.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser