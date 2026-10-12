from django.urls import path

from .views import BoardDetailView, BoardView, EmailCheckView

urlpatterns = [
    path("boards/", BoardView.as_view(), name="board-list"),
    path("boards/<int:pk>/", BoardDetailView.as_view(), name="board-detail"),
    path("email-check/", EmailCheckView.as_view(), name="email-check"),
]
