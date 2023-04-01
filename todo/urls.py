from django.urls import path
from . import views

urlpatterns = [
    path('create', views.CreateFolderView.as_view(), name='folders.create'),
    path('<int:folder_id>/tasks', views.TasksIndexView.as_view(), name='tasks.index'),  
    path('<int:folder_id>/tasks/create', views.CreateTaskView.as_view(), name='tasks.create'),
    path('<int:folder_id>/tasks/<int:task_id>', views.EditTaskView.as_view(), name='tasks.edit'),
    path('<int:folder_id>/delete', views.delete_folder, name='folders.delete'),
    path('<int:folder_id>/tasks/<int:task_id>/delete', views.delete_task, name='tasks.delete'),
    path('<int:folder_id>/update_order', views.UpdateOrderView.as_view(), name='update_order')
]