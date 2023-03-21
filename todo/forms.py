from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Folder, Task

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {
                'class': 'form-control',
                'placeholder': field.label  
            }

class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {
                'class': 'form-control',
                'placeholder': field.label  
            }

class FolderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FolderForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {
                'class': 'form-control'
            }   

    class Meta:
        model = Folder
        fields = ('title',)
        labels = {'title': 'フォルダー名'}

class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {
                'class': 'form-control'
            }

    class Meta:
        STATUS_CHICES = [(1, '未完了'), (2, '作業中'), (3, '完了')]
        model = Task
        fields = ('title', 'status', 'due_date')
        labels = {
            'title': 'タスク名',
            'status': '状態',
            'due_date': '期限',
        }