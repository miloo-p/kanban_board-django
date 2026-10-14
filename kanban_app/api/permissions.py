from rest_framework.permissions import BasePermission


class IsBoardOwnerOrMember(BasePermission):
    """
    Allows access to a board only for its owner or its members.
    """

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return obj.members.filter(pk=request.user.pk).exists()


class IsBoardOwnerOrMemberOfTask(BasePermission):
    """
    Allows access to a task only for the owner or members of the task's board.
    """

    def has_object_permission(self, request, view, obj):
        if obj.board.owner == request.user:
            return True
        return obj.board.members.filter(pk=request.user.pk).exists()


class IsAuthorOfComment(BasePermission):
    """
    Allows access to a comment only for its author.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
