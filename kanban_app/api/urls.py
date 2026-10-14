from django.urls import path

from .views import (
    AssignedToMeListView,
    BoardDetailView,
    BoardView,
    EmailCheckView,
    ReviewingListView,
    TaskCommentsView,
    TaskDetailView,
    TaskView,
)

urlpatterns = [
    path("boards/", BoardView.as_view(), name="board-list"),
    path("boards/<int:pk>/", BoardDetailView.as_view(), name="board-detail"),
    path("tasks/", TaskView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:task_id>/comments/", TaskCommentsView.as_view(), name="task-comments"),
    path(
        "tasks/<int:task_id>/comments/<int:comment_id>/",
        TaskCommentsView.as_view(),
        name="single-task-comment",
    ),
    path("email-check/", EmailCheckView.as_view(), name="email-check"),
    path("tasks/assigned-to-me/", AssignedToMeListView.as_view(), name="task-assigned-to-me"),
    path("tasks/reviewing/", ReviewingListView.as_view(), name="task-reviewing"),
]
