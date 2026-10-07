from django.contrib import admin
from .models import Board, Task


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass
