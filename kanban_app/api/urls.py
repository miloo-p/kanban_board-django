from django.urls import path

from .views import AssignedToMeListView, BoardDetailView, BoardView, EmailCheckView

urlpatterns = [
    path("boards/", BoardView.as_view(), name="board-list"),
    path("boards/<int:pk>/", BoardDetailView.as_view(), name="board-detail"),
    path("email-check/", EmailCheckView.as_view(), name="email-check"),
    path("tasks/assigned-to-me/", AssignedToMeListView.as_view(), name="assigned-to-me"),
]
