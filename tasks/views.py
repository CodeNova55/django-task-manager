from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import TaskForm
from .models import Task


class OwnerTasksMixin(LoginRequiredMixin):
    """Users can only see and change their own tasks."""

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


class TaskListView(OwnerTasksMixin, ListView):
    model = Task
    context_object_name = "tasks"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TaskUpdateView(OwnerTasksMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_list")


class TaskDeleteView(OwnerTasksMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("task_list")


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response