from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Position, Worker, Task, TaskType
from .forms import PositionForm, WorkerForm, TaskTypeForm, TaskForm

@login_required (login_url='login')
def position_list(request):
    positions = Position.objects.all()
    return render(request, 'task_manager/position_list.html', {'positions': positions})

@login_required (login_url='login')
def position_create(request):
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('position-list')
    else:
        form = PositionForm()
    return render(request, 'task_manager/position_form.html', {'form': form})

@login_required (login_url='login')
def position_delete(request, pk):
    position = get_object_or_404(Position, pk=pk)
    position.delete()
    return redirect('position-list')

@login_required (login_url='login')
def worker_list(request):
    workers = Worker.objects.all()
    return render(request, 'task_manager/worker_list.html', {'workers': workers})

@login_required (login_url='login')
def worker_detail(request, pk):
    worker = get_object_or_404(Worker, pk=pk)
    return render(request, 'task_manager/worker_detail.html', {'worker': worker})

@login_required (login_url='login')
def worker_create(request):
    if request.method == 'POST':
        form = WorkerForm(request.POST)
        if form.is_valid():
            worker = form.save(commit=False)
            worker.set_password(form.cleaned_data["password"])
            worker.save()
            return redirect('worker-list')
    else:
        form = WorkerForm()
    return render(request, 'task_manager/worker_form.html', {'form': form})

@login_required (login_url='login')
def worker_update(request, pk):
    worker = get_object_or_404(Worker, pk=pk)
    if request.method == 'POST':
        form = WorkerForm(request.POST, instance=worker)
        if form.is_valid():
            worker = form.save(commit=False)
            worker.set_password(form.cleaned_data["password"])
            worker.save()
            return redirect('worker-list')
    else:
        form = WorkerForm(instance=worker)
    return render(request, 'task_manager/worker_form.html', {'form': form})

@login_required (login_url='login')
def worker_delete(request, pk):
    worker = get_object_or_404(Worker, pk=pk)
    worker.delete()
    return redirect('worker-list')

@login_required (login_url='login')
@permission_required("IT_task_manager.view_task",
                     raise_exception=True)
def task_list(request):
    tasks = get_visible_tasks(request.user)
    return render(request, 'task_manager/task_list.html', {'tasks': tasks})

@login_required (login_url='login')
@permission_required("IT_task_manager.view_task",
                     raise_exception=True)
def task_detail(request, pk):
    task = get_object_or_404(
        get_visible_tasks(request.user),
        pk=pk,)

    return render(request, 'task_manager/task_detail.html', {'task': task})

@login_required (login_url='login')
@permission_required("IT_task_manager.add_task",
                     raise_exception=True)
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task-list")
    else:
        form = TaskForm()
    return render(request, 'task_manager/Task_form.html', {'form': form})

@login_required (login_url='login')
@permission_required("IT_task_manager.change_task",
                     raise_exception=True)
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task-list")
    else:
        form = TaskForm(instance=task)
    return render(request, "task_manager/task_form.html", {"form": form})

@login_required(login_url="login")
@permission_required(
    "IT_task_manager.complete_task",
    raise_exception=True,
)
def task_complete(request, pk):
    task = get_object_or_404(
        Task.objects.filter(assignees=request.user),
        pk=pk,
    )

    if request.method == "POST":
        task.is_completed = True
        task.save(update_fields=["is_completed"])
        return redirect("task-detail", pk=task.pk)

    return render(
        request,
        "task_manager/task_complete.html",
        {"task": task},
    )

@login_required (login_url='login')
@permission_required("IT_task_manager.delete_task",
                     raise_exception=True)
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('task-list')

@login_required (login_url='login')
def task_type_list(request):
    task_types = TaskType.objects.all()
    return render(request, 'task_manager/task_type_list.html', {'task_type': task_types})

@login_required (login_url='login')
def task_type_create(request):
    if request.method == 'POST':
        form = TaskTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task-type-list')
    else:
        form = TaskTypeForm()
    return render(request, 'task_manager/task_type_form.html', {'form': form})

@login_required (login_url='login')
def task_type_delete(request, pk):
    task_type = get_object_or_404(TaskType, pk=pk)
    task_type.delete()
    return redirect('task-type-list')

@login_required(login_url='login')
def index(request):
    tasks = get_visible_tasks(request.user)

    active_tasks = tasks.filter(is_completed=False)
    completed_tasks = tasks.filter(is_completed=True)

    workers_count = Worker.objects.count()

    return render(request, 'task_manager/index.html', {
        'active_tasks': active_tasks,
        'active_tasks_count': active_tasks.count(),
        'completed_tasks_count': completed_tasks.count(),
        'workers_count': workers_count,
    })

def get_visible_tasks(user):
    if user.groups.filter(name="Supervisor").exists():
        return (
                Task.objects.filter(assignees__supervisor=user)
                | Task.objects.filter(assignees=user)
        ).distinct()

    return Task.objects.filter(assignees=user)