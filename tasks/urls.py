from django.urls import path
from . import views

urlpatterns = [
    path('task/', views.task),              # GET all tasks / POST new task
    path('task/<int:id>/', views.task_id),  # GET/PATCH/DELETE by task ID
]
