from django.contrib.auth.models import User
from rest_framework import serializers

from kanban_app.models import Board


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


class EmailCheckSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source="profile.fullname", read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]


class EmailValidatorSerializer(serializers.Serializer):
    email = serializers.EmailField()
