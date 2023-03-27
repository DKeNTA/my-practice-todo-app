from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_folder, name='folders.create'),
    path('<int:folder_id>/tasks', views.tasks_index, name='tasks.index'),  
    path('<int:folder_id>/tasks/create', views.create_task, name='tasks.create'),
    path('<int:folder_id>/tasks/<int:task_id>', views.edit_task, name='tasks.edit'),
    path('<int:folder_id>/delete', views.delete_folder, name='folders.delete'),
    path('<int:folder_id>/tasks/<int:task_id>/delete', views.delete_task, name='tasks.delete'),
]