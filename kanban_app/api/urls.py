from django.urls import path

from .views import (
    AssignedToMeListView,
    BoardDetailView,
    BoardView,
    EmailCheckView,
    ReviewingListView,
    TaskView,
)

urlpatterns = [
    path("boards/", BoardView.as_view(), name="board-list"),
    path("boards/<int:pk>/", BoardDetailView.as_view(), name="board-detail"),
    path("tasks/", TaskView.as_view(), name="task-list"),
    path("email-check/", EmailCheckView.as_view(), name="email-check"),
    path("tasks/assigned-to-me/", AssignedToMeListView.as_view(), name="task-assigned-to-me"),
    path("tasks/reviewing/", ReviewingListView.as_view(), name="task-reviewing"),
]
