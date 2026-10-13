from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Board
from .permissions import IsOwnerOrMember
from .querysets import boards_with_counts, tasks_with_counts
from .serializer import (
    AssignedTaskSerializer,
    BoardDetailSerializer,
    BoardSerializer,
    BoardUpdateSerializer,
    EmailValidatorSerializer,
    UserSerializer,
)


class BoardView(APIView):
    """
    View to create and list Boards
    """

    def post(self, request):
        """
        View for creating a Board
        """
        serializer = BoardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        board = serializer.save(owner=request.user)
        board = boards_with_counts().get(pk=board.pk)
        return Response(BoardSerializer(board).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        """
        Alle Boards, bei denen der User Owner oder Member ist.
        Insgesamt nur eine einzige Datenbank-Query.
        """
        boards = (
            boards_with_counts().filter(Q(owner=request.user) | Q(members=request.user)).distinct()
        )
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)


class EmailCheckView(APIView):
    def get(self, request):
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
    permission_classes = [IsAuthenticated, IsOwnerOrMember]

    def get(self, request, pk):
        """
        Einzelnes Board, bei denen der User Owner oder Member ist.
        """
        board = get_object_or_404(Board, pk=pk)
        self.check_object_permissions(request, board)
        serializer = BoardDetailSerializer(board)
        return Response(serializer.data)

    def delete(self, request, pk):
        """
        Löscht einzelnes Board, bei denen der User Owner ist.
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
        Updated einzelnes Board, bei denen der User Owner oder Member ist.
        """
        board = get_object_or_404(Board, pk=pk)
        self.check_object_permissions(request, board)
        serializer = BoardUpdateSerializer(board, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AssignedToMeListView(APIView):
    def get(self, request):

        tasks = tasks_with_counts().filter(assignee=request.user)
        serializer = AssignedTaskSerializer(tasks, many=True)
        return Response(serializer.data)


class ReviewingListView(APIView):
    def get(self, request):

        tasks = tasks_with_counts().filter(reviewer=request.user)
        serializer = AssignedTaskSerializer(tasks, many=True)
        return Response(serializer.data)
