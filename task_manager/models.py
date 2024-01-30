from django.contrib.auth.models import User
from django.db import models

class Task(models.Model):
    """
    Model representing a task.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the task.
        """
        return self.title