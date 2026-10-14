from rest_framework.permissions import BasePermission


class IsBoardOwnerOrMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return obj.members.filter(pk=request.user.pk).exists()


class IsBoardOwnerOrMemberOfTask(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.board.owner == request.user:
            return True
        return obj.board.members.filter(pk=request.user.pk).exists()


class IsAuthorOfComment(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
