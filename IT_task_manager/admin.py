from django.contrib import admin
from .models import Position, Worker, TaskType
admin.site.register(Position)
admin.site.register(Worker)
admin.site.register(TaskType)