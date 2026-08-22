from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import Permission

from .models import Position, Worker, Task, TaskType


class WorkerModelTest(TestCase):
    def test_worker_str_with_position(self):
        position = Position.objects.create(name="Operator")

        worker = Worker.objects.create(
            username="kowalski",
            first_name="Jan",
            last_name="Kowalski",
            position=position,
        )

        self.assertEqual(
            str(worker),
            "Operator Jan Kowalski",
        )

    def test_worker_str_without_position(self):
        worker = Worker.objects.create(
            username="kowalski",
            first_name="Jan",
            last_name="Kowalski",
        )

        self.assertEqual(
            str(worker),
            "Brak stanowiska Jan Kowalski",
        )

from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from .models import Worker


class TaskCreatePermissionTest(TestCase):
    def setUp(self):
        self.worker = Worker.objects.create_user(
            username="kowalski",
            password="testpassword",
        )

        self.url = reverse("task-create")

        self.permission = Permission.objects.get(
            codename="add_task",
        )

    def test_worker_without_permission_gets_403(self):
        self.client.login(
            username="kowalski",
            password="testpassword",
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)

    def test_worker_with_permission_can_access(self):
        self.worker.user_permissions.add(self.permission)

        self.client.login(
            username="kowalski",
            password="testpassword",
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

class TaskCompleteTest(TestCase):
    def setUp(self):
        self.worker = Worker.objects.create_user(
            username="kowalski",
            password="testpassword",
        )

        permission = Permission.objects.get(
            codename="complete_task",
        )

        self.worker.user_permissions.add(permission)

        self.task_type = TaskType.objects.create(
            name="Test task",
        )

        self.task = Task.objects.create(
            name="Test task",
            description="Test description",
            deadline=timezone.now(),
            task_type=self.task_type,
        )

        self.task.assignees.add(self.worker)

    def test_task_can_be_completed(self):
        self.client.login(
            username="kowalski",
            password="testpassword",
        )

        response = self.client.post(
            reverse("task-complete", kwargs={"pk": self.task.pk})
        )

        self.task.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.task.is_completed)
        self.assertIsNotNone(self.task.completed_at)
