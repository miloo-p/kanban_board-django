from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Board, Comment, Task
from .permissions import IsAuthorOfComment, IsBoardOwnerOrMember, IsBoardOwnerOrMemberOfTask
from .querysets import boards_with_counts, tasks_with_counts
from .serializer import (
    BoardDetailSerializer,
    BoardSerializer,
    BoardUpdateSerializer,
    CommentSerializer,
    EmailValidatorSerializer,
    TaskSerializer,
    TaskUpdateSerializer,
    UserSerializer,
)


class BoardView(APIView):
    """
    View to create and list boards.
    """

    def post(self, request):
        """
        Creates a board with the requesting user as owner.
        """
        serializer = BoardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        board = serializer.save(owner=request.user)
        board = boards_with_counts().get(pk=board.pk)
        return Response(BoardSerializer(board).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        """
        Lists all boards where the user is owner or member.
        Uses only a single database query.
        """
        boards = (
            boards_with_counts().filter(Q(owner=request.user) | Q(members=request.user)).distinct()
        )
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)


class EmailCheckView(APIView):
    """
    View to look up a user by email.
    """

    def get(self, request):
        """
        Returns the user with the given email or 404 if no such user exists.
        """
        email_serializer = EmailValidatorSerializer(data=request.query_params)
        email_serializer.is_valid(raise_exception=True)
        email = email_serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            error_data = {"error": "Not Found", "details": f"There is no user with email: {email}."}
            return Response(error_data, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BoardDetailView(APIView):
    """
    View to retrieve, update and delete a single board.
    """

    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]

    def get(self, request, pk):
        """
        Returns a single board with members and tasks if the user is owner or member.
        """
        board = get_object_or_404(Board, pk=pk)
        self.check_object_permissions(request, board)
        serializer = BoardDetailSerializer(board)
        return Response(serializer.data)

    def delete(self, request, pk):
        """
        Deletes a single board; only the owner is allowed to do this.
        """
        board = get_object_or_404(Board, pk=pk)
        self.check_object_permissions(request, board)
        if request.user != board.owner:
            return Response(
                {"error": "Nur der Owner darf das Board löschen."}, status=status.HTTP_403_FORBIDDEN
            )
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        """
        Updates title and members of a board if the user is owner or member.
        """
        board = get_object_or_404(Board, pk=pk)
        self.check_object_permissions(request, board)
        serializer = BoardUpdateSerializer(board, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AssignedToMeListView(APIView):
    """
    View to list the tasks assigned to the requesting user.
    """

    def get(self, request):
        """
        Returns all tasks where the user is assignee.
        """
        tasks = tasks_with_counts().filter(assignee=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class ReviewingListView(APIView):
    """
    View to list the tasks the requesting user has to review.
    """

    def get(self, request):
        """
        Returns all tasks where the user is reviewer.
        """
        tasks = tasks_with_counts().filter(reviewer=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskView(APIView):
    """
    View to create tasks.
    """

    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]

    def post(self, request):
        """
        Creates a task on a board where the user is owner or member;
        the requesting user becomes the creator.
        """
        board = get_object_or_404(Board, pk=request.data.get("board"))
        self.check_object_permissions(request, board)
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save(creator=request.user)
        task = tasks_with_counts().get(pk=task.pk)
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)


class TaskDetailView(APIView):
    """
    View to update and delete a single task.
    """

    permission_classes = [IsAuthenticated, IsBoardOwnerOrMemberOfTask]

    def delete(self, request, pk):
        """
        Deletes a single task; only the board owner or the task creator is allowed to do this.
        """
        task = get_object_or_404(Task, pk=pk)
        self.check_object_permissions(request, task)
        if request.user != task.board.owner and request.user != task.creator:
            return Response(
                {
                    "error": "Nur der Creator der Task oder der Owner des Boards darf die Task löschen."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        """
        Updates a single task if the user is owner or member of the task's board.
        """
        task = get_object_or_404(Task, pk=pk)
        self.check_object_permissions(request, task)
        serializer = TaskUpdateSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TaskCommentsView(APIView):
    """
    View to list and create comments of a task.
    """

    permission_classes = [IsAuthenticated, IsBoardOwnerOrMemberOfTask]

    def get(self, request, task_id):
        """
        Returns all comments of a task if the user is owner or member of its board.
        """
        task = get_object_or_404(Task, pk=task_id)
        self.check_object_permissions(request, task)
        comments = task.comments.all()
        serializer = CommentSerializer(comments, many=True)

        return Response(serializer.data)

    def post(self, request, task_id):
        """
        Creates a comment on a task with the requesting user as author.
        """
        task = get_object_or_404(Task, pk=task_id)
        self.check_object_permissions(request, task)
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(task=task, author=request.user)
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)


class TaskCommentDetailView(APIView):
    """
    View to delete a single comment of a task.
    """

    permission_classes = [IsAuthenticated, IsAuthorOfComment]

    def delete(self, request, task_id, comment_id):
        """
        Deletes a comment; only its author is allowed to do this.
        """
        comment = get_object_or_404(Comment, task=task_id, pk=comment_id)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
