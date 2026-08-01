from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from .models import Position, Worker, Task, TaskType
from .forms import PositionForm, WorkerForm


def position_list(request):
    positions = Position.objects.all()
    return render(request, 'task_manager/position_list.html', {'positions': positions})

def position_create(request):
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('position-list')
    else:
        form = PositionForm()
    return render(request, 'task_manager/position_form.html', {'form': form})

def position_delete(request, pk):
    position = get_object_or_404(Position, pk=pk)
    position.delete()
    return redirect('position-list')

def worker_list(request):
    workers = Worker.objects.all()
    return render(request, 'task_manager/worker_list.html', {'workers': workers})

def worker_detail(request, pk):
    worker = get_object_or_404(Worker, pk=pk)
    return render(request, 'task_manager/worker_detail.html', {'worker': worker})

def worker_create(request):
    if request.method == 'POST':
        form = WorkerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('worker-list')
    else:
        form = WorkerForm()
    return render(request, 'task_manager/worker_form.html', {'form': form})

def worker_delete(request, pk):
    worker = get_object_or_404(Worker, pk=pk)
    worker.delete()
    return redirect('worker-list')

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_manager/task_list.html', {'tasks': tasks})

def task_type_list(request):
    task_types = TaskType.objects.all()
    return render(request, 'task_manager/task_types_list.html', {'task_types': task_types})