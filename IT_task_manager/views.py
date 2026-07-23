from django.shortcuts import render
from .models import Position, Worker
def position_list(request):
    positions = Position.objects.all()
    return render(request, 'task_manager/position_list.html', {'positions': positions})
def worker_list(request):
    workers = Worker.objects.all()
    return render(request, 'task_manager/worker_list.html', {'workers': workers})