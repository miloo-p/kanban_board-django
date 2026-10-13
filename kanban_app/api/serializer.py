from django.contrib.auth.models import User
from rest_framework import serializers

from kanban_app.models import Board, Task

from .querysets import tasks_with_counts


class BoardSerializer(serializers.ModelSerializer):
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
    fullname = serializers.CharField(source="profile.fullname", read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]


class EmailValidatorSerializer(serializers.Serializer):
    email = serializers.EmailField()


class TaskCurrentBoardSerializer(serializers.ModelSerializer):
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
    class Meta(TaskCurrentBoardSerializer.Meta):
        fields = [
            "id",
            "board",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "due_date",
            "comments_count",
        ]


class BoardDetailSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ["id", "title", "owner_id", "members", "tasks"]

    def get_tasks(self, obj):
        tasks = tasks_with_counts().filter(board=obj)
        serializer = TaskCurrentBoardSerializer(tasks, many=True)
        return serializer.data


class BoardUpdateSerializer(serializers.ModelSerializer):
    owner_data = UserSerializer(source="owner", read_only=True)
    members_data = UserSerializer(source="owner", many=True, read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "owner_data", "members_data", "members"]
        extra_kwargs = {"members": {"write_only": True}}
