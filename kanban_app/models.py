from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Board(models.Model):
    title = models.CharField(max_length=100)
    members = models.ManyToManyField(
        User, related_name='member_of', blank=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='owner_of')

    def __str__(self):
        return self.title


class Task(models.Model):
    STATUS_CHOICES = [
        ('to-do', 'To do'),
        ('in-progress', 'In progress'),
        ('review', 'Review'),
        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='to-do')
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateField()
    assignee = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='assigned_to', null=True, blank=True)
    reviewer = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='reviews', null=True, blank=True)
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name='tasks')
    creator = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='created_tasks')

    def __str__(self):
        return self.title
