from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from tasks import models
from tasks.forms import TaskForm
from tasks.mixins import UserIsExecutorMixin, UserIsOwnerMixin

# Create your views here.
class TaskListView(ListView):
    model = models.Task
    context_object_name = 'tasks'
    template_name = 'tasks/task_list.html'

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = models.Task
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task-list')
    form_class = TaskForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = models.Task
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task-list')
    form_class = TaskForm


# class TaskDeleteView(LoginRequiredMixin, DeleteView):
