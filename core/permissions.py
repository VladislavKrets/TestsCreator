from rest_framework import permissions
from datetime import datetime
from core import models


class IsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        is_authenticated = bool(request.user and request.user.is_authenticated)
        try:
            last_login = request.user.last_login
            now = datetime.now()
            if is_authenticated and (last_login is None or last_login.date() != now.date()):
                request.user.last_login = now
                request.user.save()
        except AttributeError:
            pass
        return is_authenticated


class IsGroupOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        is_group_administrator = models.TestUserForGroup.objects.filter(
            user=user.testuser,
            group__id=request.resolver_match.kwargs.get('group', "-1"),
            user_role=models.TestUserForGroup.UserRoles.ADMINISTRATOR).exists()
        return is_group_administrator


class IsGroupMember(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        is_group_member = models.TestUserForGroup.objects.filter(
            user=user.testuser,
            group__id=request.resolver_match.kwargs.get('group', "-1"))
        return is_group_member
