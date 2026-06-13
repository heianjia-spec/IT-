from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Only admin users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsAdminOrAssetManager(permissions.BasePermission):
    """Admin or asset manager can write."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role in ('admin', 'asset_manager')


class IsAdminOrManagerOrUser(permissions.BasePermission):
    """Admin, asset manager can write; normal user can write; viewer read-only."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role in ('admin', 'asset_manager', 'user')
