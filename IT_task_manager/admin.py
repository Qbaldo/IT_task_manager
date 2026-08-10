from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Position, Worker, TaskType, Task


admin.site.register(Position)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Company", {"fields": ("position", "supervisor")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Company", {"fields": ("position", "supervisor")}),
    )

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        obj = form.instance
        if obj.position and obj.position.group:
            obj.groups.set([obj.position.group])


admin.site.register(TaskType)
admin.site.register(Task)

