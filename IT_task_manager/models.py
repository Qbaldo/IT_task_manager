from django.db import models
from django.contrib.auth.models import AbstractUser


class Position(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        position_name = self.position.name if self.position else "Brak stanowiska"
        return f"{position_name} {self.first_name} {self.last_name}"


class TaskType(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Task(models.Model):
    class Priority(models.IntegerChoices):
        LOW = 1
        MEDIUM = 2
        HIGH = 3

    name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.MEDIUM)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Worker)
    class Meta:
        ordering = ["name"]
    def __str__(self):
        return f"{self.task_type.name} {self.name}"