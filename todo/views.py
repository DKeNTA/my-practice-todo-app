from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Folder, Task
from .forms import RegisterForm, LoginForm, FolderForm, TaskForm

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid
    
class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'authentication/login.html'

class LogoutView(LogoutView):
    template_name = 'authentication/login.html'

class IndexView(LoginRequiredMixin, ListView):
    model = Folder
    template_name = 'index.html'
    context_object_name = 'folders'

    def get_queryset(self):
        return Folder.objects.filter(user=self.request.user, created_at__lte=timezone.now()).order_by('created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = None
        context['current_folder_id'] = None
        return context

class TasksIndexView(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        current_folder = get_object_or_404(Folder, id=self.kwargs['folder_id'], user=self.request.user)
        return Task.objects.filter(folder_id=current_folder.id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['folders'] = Folder.objects.filter(user=self.request.user, created_at__lte=timezone.now()).order_by('created_at')
        context['current_folder_id'] = self.kwargs['folder_id']
        return context
    
class CreateFolderView(LoginRequiredMixin, CreateView):
    model = Folder
    form_class = FolderForm
    template_name = 'create_folders.html'

    def form_valid(self, form):
        folder = form.save(commit=False)
        folder.user = self.request.user
        folder.created_at = timezone.now()
        folder.save()
        return redirect('tasks.index', folder_id=folder.id)
    
class CreateTaskView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'create_tasks.html'

    def form_valid(self, form):
        task = form.save(commit=False)
        task.created_at = timezone.now()
        task.folder = get_object_or_404(Folder, id=self.kwargs['folder_id'], user=self.request.user)
        task.save()
        return redirect('tasks.index', folder_id=task.folder.id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['folders'] = Folder.objects.filter(user=self.request.user, created_at__lte=timezone.now()).order_by('created_at')
        context['current_folder_id'] = self.kwargs['folder_id']
        return context

class EditTaskView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'edit_tasks.html'

    def form_valid(self, form):
        task = form.save(commit=False)
        task.save()
        return redirect('tasks.index', folder_id=task.folder.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['folders'] = Folder.objects.filter(user=self.request.user, created_at__lte=timezone.now()).order_by('created_at')
        context['current_folder_id'] = self.kwargs['folder_id']
        context['task_id'] = self.kwargs['task_id']
        return context
    
    def get_object(self, queryset=None):
        return get_object_or_404(Task, id=self.kwargs['task_id'])

@login_required
def delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    folder.delete()
    return redirect('folders.index')

@login_required
def delete_task(request, folder_id, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.folder.user != request.user:
        raise PermissionDenied
    task.delete()
    return redirect('tasks.index', folder_id=folder_id)
