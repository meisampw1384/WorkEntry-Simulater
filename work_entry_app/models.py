from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Board(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class List(models.Model):
    name = models.CharField(max_length=100)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='lists')
    
    def __str__(self):
        return self.name


class Card(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(blank=True , null = True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='cards')
    completed = models.BooleanField(default = False)
    
    def __str__(self):
        return self.name
    
    def is_overdue(self):
        return self.end_time < timezone.now() and not self.completed
