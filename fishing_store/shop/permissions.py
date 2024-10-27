from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Разрешает доступ к GET-запросам всем пользователям,
    но ограничивает остальные действия только для админов.
    """
    def has_permission(self, request, view):
        # Разрешает доступ к GET-запросам
        if request.method in SAFE_METHODS:
            return True
        # Для остальных запросов проверяет, является ли пользователь админом
        return request.user and request.user.is_staff
