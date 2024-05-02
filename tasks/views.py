from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from tasks import models
from tasks.forms import TaskForm, TaskFilterForm, CommentCreateForm
from tasks.mixins import UserIsExecutorMixin, UserIsOwnerMixin

# Create your views here.
class TaskListView(LoginRequiredMixin, ListView):
    model = models.Task
    context_object_name = 'tasks'
    template_name = 'tasks/task_list.html'

    def get_queryset(self):
        queryset = super(TaskListView, self).get_queryset()

        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status= status)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskFilterForm(self.request.GET)
        return context

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
    template_name = 'tasks/task_detail.html'
    success_url = reverse_lazy('tasks:task-list')
    form_class = TaskForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentCreateForm()
        return context

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Task
    template_name = 'tasks/delete_confirmation.html'
    success_url = reverse_lazy('tasks:task-list')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = models.Comment
    form_class = CommentCreateForm

    def get_success_url(self):
        return  reverse_lazy('tasks:task-update', kwargs={'pk': self.object.task.pk})

    def get_task(self):
        task_pk = self.kwargs.get('pk')
        return get_object_or_404(models.Task, pk=task_pk)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.task = self.get_task()
        return super().form_valid(form)


