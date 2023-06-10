from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsAdmin(BasePermission):
    message = "Эти действия не разрешены пользователям"

    def has_object_permission(self, request, view, obj):
        if request.user.role == UserRoles.ADMIN:
            return True


class IsOwner(BasePermission):
    message = "Вы не можете вносить изменения в чужие данные"

    def has_object_permission(self, request, view, obj):
        owner = obj.author
        if request.user == owner:
            return True
