from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Position, Worker, Task, TaskType
from .forms import PositionForm, WorkerForm, TaskTypeForm, TaskForm


@login_required(login_url="login")
@permission_required(
    "IT_task_manager.view_position",
    raise_exception=True,
)
def position_list(request):
    positions = Position.objects.all()
    return render(
        request,
        "task_manager/position_list.html",
        {"positions": positions},
    )


@login_required(login_url="login")
@permission_required(
    "IT_task_manager.add_position",
    raise_exception=True,
)
def position_create(request):
    if request.method == "POST":
        form = PositionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("position-list")
    else:
        form = PositionForm()

    return render(
        request,
        "task_manager/position_form.html",
        {"form": form},
    )


@login_required(login_url="login")
@permission_required(
    "IT_task_manager.change_position",
    raise_exception=True,
)
def position_update(request, pk):
    position = get_object_or_404(Position, pk=pk)

    if request.method == "POST":
        form = PositionForm(request.POST, instance=position)

        if form.is_valid():
            form.save()
            return redirect("position-list")
    else:
        form = PositionForm(instance=position)

    return render(
        request,
        "task_manager/position_form.html",
        {"form": form},
    )


@login_required(login_url="login")
@permission_required(
    "IT_task_manager.delete_position",
    raise_exception=True,
)
def position_delete(request, pk):
    position = get_object_or_404(Position, pk=pk)

    if position.worker_set.exists():
        return redirect("position-list")

    position.delete()
    return redirect("position-list")


@login_required(login_url="login")
@permission_required(
  "IT_task_manager.view_worker",
  raise_exception=True,
)
def worker_list(request):
    workers = get_team(request.user)

    workers = sorted(
        workers,
        key=lambda worker: (
            worker.position.name if worker.position else "",
            worker.last_name,
            worker.first_name,
        ),
    )

    return render(request,
                  "task_manager/worker_list.html",
                  {"workers": workers}
                  )


@login_required(login_url="login")
def worker_detail(request, pk):
    worker = get_object_or_404(Worker, pk=pk)

    if worker.pk != request.user.pk:
        if not request.user.has_perm("IT_task_manager.view_worker"):
            raise PermissionDenied

    return render(request,
                  "task_manager/worker_detail.html",
                  {"worker": worker})


@login_required(login_url="login")
@permission_required(
    "IT_task_manager.add_worker",
    raise_exception=True,
)
def worker_create(request):
    if request.method == "POST":
        form = WorkerForm(request.POST)
        if form.is_valid():
            worker = form.save(commit=False)
            worker.set_password(form.cleaned_data["password"])
            worker.save()
            return redirect("worker-list")
    else:
        form = WorkerForm()

    return render(
        request,
        "task_manager/worker_form.html",
        {"form": form},
    )


@login_required(login_url="login")
@permission_required(
    "IT_task_manager.change_worker",
    raise_exception=True,
)
def worker_update(request, pk):
    worker = get_object_or_404(Worker, pk=pk)

    if request.method == "POST":
        form = WorkerForm(request.POST, instance=worker)
        if form.is_valid():
            worker = form.save(commit=False)
            worker.set_password(form.cleaned_data["password"])
            worker.save()
            return redirect("worker-list")
    else:
        form = WorkerForm(instance=worker)

    return render(
        request,
        "task_manager/worker_form.html",
        {"form": form},
    )


@login_required(login_url="login")
@permission_required(
    "IT_task_manager.delete_worker",
    raise_exception=True,
)
def worker_delete(request, pk):
    worker = get_object_or_404(Worker, pk=pk)
    worker.delete()
    return redirect("worker-list")


@login_required(login_url="login")
@permission_required(
    "IT_task_manager.view_task",
    raise_exception=True,
)
def task_list(request):
    tasks = get_visible_tasks(request.user)

    active_tasks = sorted(
        [task for task in tasks if not task.is_completed],
        key=lambda task: (
            -task.priority,
            task.deadline,
            task.name,
        ),
    )[:20]

    completed_tasks = [
        task
        for task in tasks
        if task.is_completed
    ]

    history_with_date = sorted(
        [
            task
            for task in completed_tasks
            if task.completed_at is not None
        ],
        key=lambda task: task.completed_at,
        reverse=True,
    )

    history_without_date = [
        task
        for task in completed_tasks
        if task.completed_at is None
    ]

    history_tasks = (
        history_with_date + history_without_date
    )[:15]

    return render(
        request,
        "task_manager/task_list.html",
        {
            "active_tasks": active_tasks,
            "history_tasks": history_tasks,
        },
    )


@login_required(login_url='login')
@permission_required("IT_task_manager.view_task",
                     raise_exception=True)
def task_detail(request, pk):
    task = get_object_or_404(
        get_visible_tasks(request.user),
        pk=pk,)

    return render(request, 'task_manager/task_detail.html', {'task': task})


@login_required(login_url='login')
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


@login_required(login_url='login')
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
        get_visible_tasks(request.user),
        pk=pk,
    )

    if request.method == "POST":
        task.is_completed = True
        task.completed_at = timezone.now()
        task.save(update_fields=["is_completed", "completed_at"])
        return redirect("task-detail", pk=task.pk)

    return render(
        request,
        "task_manager/task_complete.html",
        {"task": task},
    )


@login_required(login_url='login')
@permission_required("IT_task_manager.delete_task",
                     raise_exception=True)
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('task-list')


@login_required(login_url="login")
@permission_required(
    "IT_task_manager.view_tasktype",
    raise_exception=True,
)
def task_type_list(request):
    active_task_types = TaskType.objects.filter(is_active=True)
    inactive_task_types = TaskType.objects.filter(is_active=False)

    return render(
        request,
        "task_manager/task_type_list.html",
        {
            'active_task_types': active_task_types,
            'inactive_task_types': inactive_task_types,
        },
    )


@login_required(login_url='login')
@permission_required(
    "IT_task_manager.add_tasktype",
    raise_exception=True,
)
def task_type_create(request):
    if request.method == 'POST':
        form = TaskTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task-type-list')
    else:
        form = TaskTypeForm()

    return render(request, 'task_manager/task_type_form.html', {'form': form})


@login_required(login_url="login")
@permission_required(
    "IT_task_manager.change_tasktype",
    raise_exception=True,
)
def task_type_update(request, pk):
    task_type = get_object_or_404(TaskType, pk=pk)

    if request.method == "POST":
        form = TaskTypeForm(request.POST, instance=task_type)

        if form.is_valid():
            form.save()
            return redirect("task-type-list")
    else:
        form = TaskTypeForm(instance=task_type)

    return render(
        request,
        "task_manager/task_type_form.html",
        {"form": form},
    )


@login_required(login_url="login")
@permission_required(
    "IT_task_manager.delete_tasktype",
    raise_exception=True,
)
def task_type_delete(request, pk):
    task_type = get_object_or_404(TaskType, pk=pk)
    task_type.is_active = False
    task_type.save(update_fields=["is_active"])
    return redirect("task-type-list")


@login_required(login_url="login")
def index(request):
    tasks = get_visible_tasks(request.user)

    now = timezone.now()

    active_tasks = list(
        tasks.filter(
            is_completed=False,
        ).order_by(
            "-priority",
            "deadline",
            "name",
        )[:20]
    )

    for task in active_tasks:
        if task.deadline < now:
            task.deadline_status = "overdue"
        elif task.deadline <= now + timedelta(hours=24):
            task.deadline_status = "soon"
        else:
            task.deadline_status = "normal"

    completed_today_count = tasks.filter(
        is_completed=True,
        completed_at__date=timezone.localdate(),
    ).count()

    overdue_tasks_count = tasks.filter(
        is_completed=False,
        deadline__lt=now,
    ).count()

    return render(
        request,
        "task_manager/index.html",
        {
            "active_tasks": active_tasks,
            "active_tasks_count": tasks.filter(is_completed=False).count(),
            "completed_today_count": completed_today_count,
            "overdue_tasks_count": overdue_tasks_count,
        },
    )


def get_visible_tasks(user):
    team = get_team(user)

    return Task.objects.filter(
        assignees__in=list(team) + [user]
    ).distinct()


def get_team(user):
    team = set()

    def add_team(worker):
        for member in worker.team.all():
            if member not in team:
                team.add(member)
                add_team(member)

    add_team(user)

    return team
