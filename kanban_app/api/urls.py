from django.urls import path
from .views import BoardListCreateView, EmailCheckView

urlpatterns = [
    path('boards/', BoardListCreateView.as_view(),
         name='board-list'),
    path('email-check/', EmailCheckView.as_view(),
         name='email-check'),

]
