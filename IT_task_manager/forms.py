

from django import forms
from .models import Position, Worker, TaskType


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = '__all__'


class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = '__all__'

class TaskTypeForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = '__all__'
