from rest_framework import generics
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import BoardSerializer, EmailCheckSerializer, EmailValidatorSerializer
from ..models import Board, User


class BoardListCreateView(generics.ListCreateAPIView):
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(Q(owner=self.request.user) | Q(members=self.request.user)).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EmailCheckView(APIView):

    def get(self, request):
        email_serializer = EmailValidatorSerializer(data=request.query_params)
        email_serializer.is_valid(raise_exception=True)
        email = email_serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            error_data = {
                "error": "Not Found",
                "details": f"There is no user with email: {email}."
            }
            return Response(error_data, status=status.HTTP_404_NOT_FOUND)
        serializer = EmailCheckSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
