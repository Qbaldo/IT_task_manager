

from django import forms
from .models import Position, Worker


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = '__all__'

class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = '__all__'