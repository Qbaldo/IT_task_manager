from django.shortcuts import render
from .models import Position, Worker, Task, TaskType


def position_list(request):
    positions = Position.objects.all()
    return render(request, 'task_manager/position_list.html', {'positions': positions})

def worker_list(request):
    workers = Worker.objects.all()
    return render(request, 'task_manager/worker_list.html', {'workers': workers})

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_manager/task_list.html', {'tasks': tasks})

def task_type_list(request):
    task_types = TaskType.objects.all()
    return render(request, 'task_manager/task_types_list.html', {'task_types': task_types})