from rest_framework.permissions import BasePermission


class IsOwnerOrMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return obj.members.filter(pk=request.user.pk).exists()
