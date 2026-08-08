from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Position, Worker, TaskType, Task


admin.site.register(Position)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    pass


admin.site.register(TaskType)
admin.site.register(Task)

