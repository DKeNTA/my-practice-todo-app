from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Folder, Task
from .forms import RegisterForm, LoginForm, FolderForm, TaskForm

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid
    
class Login(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'

class Logout(LogoutView):
    template_name = 'registration/login.html'

@login_required
def index(request):
    # 全てのフォルダを取得する
    folders = Folder.objects.filter(user=request.user, created_at__lte=timezone.now()).order_by('created_at')  # lte: less than or equal to

    return render(request, 'index.html', {
        'folders': folders,
        'tasks': None,
        'current_folder_id': None
        })

@login_required
def tasks_index(request, id):
    # 全てのフォルダを取得する
    folders = Folder.objects.filter(user=request.user, created_at__lte=timezone.now()).order_by('created_at')  # lte: less than or equal to
    # 選ばれたフォルダを取得する
    current_folder = get_object_or_404(Folder, id=id, user=request.user)
    # 選ばれたフォルダのタスクを取得する
    tasks = Task.objects.filter(folder_id=current_folder.id)

    return render(request, 'index.html', {
        'folders': folders,
        'tasks': tasks,
        'current_folder_id': current_folder.id
        })

def create_folder(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user
            folder.created_at = timezone.now()
            folder.save()
            return redirect('tasks.index', id=folder.id)
    else:
        form = FolderForm()
    return render(request, 'create_folders.html', {'form': form})

def create_task(request, id):
    folders = Folder.objects.filter(user=request.user, created_at__lte=timezone.now()).order_by('created_at') 
    # 選ばれだフォルダを取得する
    current_folder = get_object_or_404(Folder, id=id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_at = timezone.now()
            task.folder = current_folder
            task.save()
            return redirect('tasks.index', id=current_folder.id)
    else:
        form = TaskForm()
    return render(request, 'create_tasks.html', {
        'folders': folders,
        'form': form,
        'current_folder_id': current_folder.id
    })

def edit_task(request, id, task_id):
    folders = Folder.objects.filter(user=request.user, created_at__lte=timezone.now()).order_by('created_at')
    # 選ばれたタスクを取得する
    current_folder = get_object_or_404(Folder, id=id, user=request.user)
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('tasks.index', id=task.folder.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_tasks.html', {
        'folders': folders,
        'form': form,
        'current_folder_id': current_folder.id,
        'task': task
    })