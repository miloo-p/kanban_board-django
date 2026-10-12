from django.contrib.auth.models import User
from django.db.models import Count, Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Board
from .serializer import BoardSerializer, EmailCheckSerializer, EmailValidatorSerializer


def boards_with_counts():
    return Board.objects.annotate(
        member_count=Count("members", distinct=True),
        ticket_count=Count("tasks", distinct=True),
        tasks_to_do_count=Count(
            "tasks",
            filter=Q(tasks__status="to-do"),
            distinct=True,
        ),
        tasks_high_prio_count=Count(
            "tasks",
            filter=Q(tasks__priority="high"),
            distinct=True,
        ),
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
        # der Serializer bekommt die Werte aus der URL (?email=…) zum prüfen
        email_serializer = EmailValidatorSerializer(data=request.query_params)
        # Es wird geschaut ob die Anfrage wirklich eine email ist, falls nicht wird ein Error ausgegeben (400)
        email_serializer.is_valid(raise_exception=True)
        # jetzt wird die validierte Mail in eine neue Variable namens mail geschrieben
        email = email_serializer.validated_data["email"]

        try:
            # hier wird in der User Tabelle geschaut ob es einen User gibt mit der angefragten mail aus (email)
            user = User.objects.get(email=email)
            # hier wird der Fall abgesichert, sollte es die mail nicht geben bzw. das die angefragte mail nie einem user zugeordnet wurde
        except User.DoesNotExist:
            error_data = {"error": "Not Found", "details": f"There is no user with email: {email}."}
            # das ist der Ort wo definiert wird aus ausgegeben wird wenn die mail nicht existiert
            return Response(error_data, status=status.HTTP_404_NOT_FOUND)
        # der serializer bekommt den kompletten User und baut user für den Response (hier: id, email, fullname)
        serializer = EmailCheckSerializer(user)
        # Mail wurde ja gefunden, und wird hier korrekt ausgegeben wie es der response im endpunkt verlangt
        return Response(serializer.data, status=status.HTTP_200_OK)
