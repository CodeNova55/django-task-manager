from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Task

User = get_user_model()


class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("njeri", password="pass12345")

    def test_str_returns_title(self):
        task = Task.objects.create(owner=self.user, title="Write tests")
        self.assertEqual(str(task), "Write tests")

    def test_default_status_is_todo(self):
        task = Task.objects.create(owner=self.user, title="Check default")
        self.assertEqual(task.status, Task.Status.TODO)


class TaskViewTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user("alice", password="pass12345")
        self.bob = User.objects.create_user("bob", password="pass12345")
        self.alice_task = Task.objects.create(owner=self.alice, title="Alice task")
        self.bob_task = Task.objects.create(owner=self.bob, title="Bob task")

    def login_alice(self):
        self.client.login(username="alice", password="pass12345")

    def test_list_requires_login(self):
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_user_sees_only_own_tasks(self):
        self.login_alice()
        response = self.client.get(reverse("task_list"))
        self.assertContains(response, "Alice task")
        self.assertNotContains(response, "Bob task")

    def test_create_task_sets_owner(self):
        self.login_alice()
        self.client.post(
            reverse("task_create"), {"title": "New task", "status": "todo"}
        )
        self.assertTrue(
            Task.objects.filter(title="New task", owner=self.alice).exists()
        )

    def test_cannot_edit_other_users_task(self):
        self.login_alice()
        response = self.client.get(reverse("task_update", args=[self.bob_task.pk]))
        self.assertEqual(response.status_code, 404)

    def test_cannot_delete_other_users_task(self):
        self.login_alice()
        response = self.client.post(reverse("task_delete", args=[self.bob_task.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Task.objects.filter(pk=self.bob_task.pk).exists())