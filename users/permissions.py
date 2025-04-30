from rest_framework import permissions


class IsModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Разрешаем GET-запросы всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Проверяем, является ли пользователь модератором
        return request.user.groups.filter(name='moderators').exists()


class IsOwnerOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешаем GET-запросы всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Проверяем, является ли пользователь владельцем или модератором
        return obj.owner == request.user or request.user.groups.filter(name='moderators').exists()
