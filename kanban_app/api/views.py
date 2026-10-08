from rest_framework import generics
from django.db.models import Q
from .serializer import BoardSerializer
from ..models import Board


class BoardListCreateView(generics.ListCreateAPIView):
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(Q(owner=self.request.user) | Q(members=self.request.user)).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
