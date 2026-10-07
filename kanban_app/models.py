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
