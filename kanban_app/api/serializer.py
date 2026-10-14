from django.contrib.auth.models import User
from rest_framework import serializers

from kanban_app.models import Board, Comment, Task

from .querysets import tasks_with_counts


class BoardSerializer(serializers.ModelSerializer):
    """
    Serializes boards for the board list and for creating a board, including the counts
    annotated by boards_with_counts().
    """

    member_count = serializers.IntegerField(read_only=True)
    ticket_count = serializers.IntegerField(read_only=True)
    tasks_to_do_count = serializers.IntegerField(read_only=True)
    tasks_high_prio_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "member_count",
            "ticket_count",
            "tasks_to_do_count",
            "tasks_high_prio_count",
            "owner_id",
            "members",
        ]
        extra_kwargs = {"members": {"write_only": True}}


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes a user with id, email and the full name from the profile.
    """

    fullname = serializers.CharField(source="profile.fullname", read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]


class EmailValidatorSerializer(serializers.Serializer):
    """
    Validates the email query parameter of the email check.
    """

    email = serializers.EmailField()


class TaskCurrentBoardSerializer(serializers.ModelSerializer):
    """
    Read-only task representation used inside the board detail, without the board field.
    """

    assignee = UserSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "due_date",
            "comments_count",
        ]


class TaskSerializer(TaskCurrentBoardSerializer):
    """
    Serializes tasks for creating and listing; assignee and reviewer are written via
    assignee_id/reviewer_id and returned as nested users.
    """

    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="assignee",
        write_only=True,
        allow_null=True,
        required=False,
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="reviewer",
        write_only=True,
        allow_null=True,
        required=False,
    )

    class Meta(TaskCurrentBoardSerializer.Meta):
        fields = [
            "id",
            "board",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "assignee_id",
            "reviewer",
            "reviewer_id",
            "due_date",
            "comments_count",
        ]

    def validate(self, data):
        """
        Ensures that assignee and reviewer are owner or member of the task's board.
        """
        board = data.get("board", getattr(self.instance, "board", None))
        assignee = data.get("assignee")
        reviewer = data.get("reviewer")

        if assignee and not (
            board.owner == assignee or board.members.filter(pk=assignee.pk).exists()
        ):
            raise serializers.ValidationError(
                {"assignee_id": "Assignee ist kein Mitglied vom Board"}
            )
        if reviewer and not (
            board.owner == reviewer or board.members.filter(pk=reviewer.pk).exists()
        ):
            raise serializers.ValidationError(
                {"reviewer_id": "Reviewer ist kein Mitglied vom Board"}
            )
        return data


class BoardDetailSerializer(serializers.ModelSerializer):
    """
    Serializes a single board with its members and tasks.
    """

    members = UserSerializer(many=True, read_only=True)
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ["id", "title", "owner_id", "members", "tasks"]

    def get_tasks(self, obj):
        """
        Returns the board's tasks including their comment count.
        """
        tasks = tasks_with_counts().filter(board=obj)
        serializer = TaskCurrentBoardSerializer(tasks, many=True)
        return serializer.data


class BoardUpdateSerializer(serializers.ModelSerializer):
    """
    Updates title and members of a board; members are written as ids and returned
    as nested users in members_data.
    """

    owner_data = UserSerializer(source="owner", read_only=True)
    members_data = UserSerializer(source="members", many=True, read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "owner_data", "members_data", "members"]
        extra_kwargs = {"members": {"write_only": True}}


class TaskUpdateSerializer(TaskSerializer):
    """
    Updates a task; same validation as TaskSerializer, but the board cannot be changed.
    """

    class Meta(TaskSerializer.Meta):
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "assignee_id",
            "reviewer",
            "reviewer_id",
            "due_date",
        ]


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializes a comment with the author's full name.
    """

    author = serializers.CharField(source="author.profile.fullname", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "created_at", "author", "content"]
