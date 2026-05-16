# apps/accounts/permissions.py
from typing import Any

from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsTeamLeadOrAdmin(BasePermission):
    """
    Разрешает доступ на изменение (POST, PUT, PATCH, DELETE) только пользователям
    с ролью 'team_lead' или 'admin'. Обычные пользователи могут только читать (GET, HEAD, OPTIONS).
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        # Если метод безопасный (GET, HEAD, OPTIONS) — пускаем всех авторизованных
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)

        # Для мутирующих методов проверяем роль
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "role", "") in ["team_lead", "admin"]
        )


class IsProjectOwnerOrReadOnly(BasePermission):
    """
    Object-level permission. Разрешает редактировать объект (Проект/Задача)
    только его создателю (владельцу). Остальным — только просмотр.
    """

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        # Читать могут все авторизованные
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)

        # Проверяем, является ли текущий юзер создателем объекта.
        # (Предполагаем, что в будущих моделях проектов/тасок поле будет называться 'creator' или 'owner')
        owner = getattr(obj, "creator", None) or getattr(obj, "owner", None)

        return bool(
            request.user and request.user.is_authenticated and owner == request.user
        )
