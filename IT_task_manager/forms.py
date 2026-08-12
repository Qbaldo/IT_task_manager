from django import forms
from .models import Position, Worker, TaskType, Task


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = '__all__'


class WorkerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Worker
        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "position",
            "supervisor",
        ]

class TaskTypeForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = '__all__'

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"

        widgets = {
            "deadline": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                }
            ),
            "assignees": forms.SelectMultiple(
                attrs={
                    "class": "form-select",
                    "size": 5,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        queryset = TaskType.objects.filter(is_active=True)

        if self.instance and self.instance.pk:
            queryset = queryset | TaskType.objects.filter(
                pk=self.instance.task_type_id
            )

        self.fields["task_type"].queryset = queryset.distinct()