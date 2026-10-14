from django.db.models import Count, Q

from ..models import Board, Task


def boards_with_counts():
    """
    Returns all boards annotated with member, ticket, to-do and high-priority task counts,
    so the counts are computed in the same database query.
    """
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


def tasks_with_counts():
    """
    Returns all tasks annotated with their number of comments.
    """
    return Task.objects.annotate(
        comments_count=Count(
            "comments",
        ),
    )
