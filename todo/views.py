from django.shortcuts import render
from django.utils import timezone
from .models import Folder

def index(request, id):
    folders = Folder.objects.filter(created_at__lte=timezone.now()).order_by('created_at')  # lte: less than or equal to
    return render(request, 'index.html', {'folders':folders})
