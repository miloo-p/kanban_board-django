from django.urls import path

from .views import BoardView, EmailCheckView

urlpatterns = [
    path("boards/", BoardView.as_view(), name="board-list"),
    path("email-check/", EmailCheckView.as_view(), name="email-check"),
]
