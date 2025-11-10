from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import IntegrityError
import json
from tasks.models import Task
from django.db import models
from datetime import datetime


def convert_Task_to_JSON(tasks):
    if isinstance(tasks, models.Model):
        tasks = [tasks]
    
    elif isinstance(tasks, models.QuerySet):
        tasks = list(tasks)

    if not tasks:
        return []

    data = [{
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "due_date": task.due_date,
        "user": task.user,
        "completed": task.completed
    } for task in tasks]

    return data

### The method the base url uses, takes care of GET and POST
@csrf_exempt
def task(request):
    params = {}
    
    if request.method == "GET":
        if request.body:
            try:
                body = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format"}, status=400)
            title, due_date, priority, user = body.get("title"), body.get("due_date"), body.get("priority"), body.get("user")

            if title:
                params['title'] = title
            if due_date:
                params['due_date'] = datetime.strptime(due_date, "%Y-%m-%d").date()
            if priority:
                params['priority'] = int(priority)
            if user:
                params['user'] = user
        tasks = Task.objects.filter(**params)
        tasks_list = convert_Task_to_JSON(tasks)
        return JsonResponse(tasks_list, safe=False, status=200)

    if request.method == "POST":
        if not request.body:
            return JsonResponse({"error": "No JSON body provided"}, status=400)

        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        
        uid, title, description, priority, due_date, user = body.get("id"), body.get("title"), body.get("description"), body.get("priority"), body.get("due_date"), body.get("user")
        if uid is None or title is None or description is None or priority is None or due_date is None or user is None:
            return JsonResponse({"error":"Missing or invalid input"}, status=400)
        
        priority = int(priority)
        due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        try:
            Task.objects.create(id=uid, title=title, description=description, priority=priority, due_date=due_date, user=user, completed=False)
            return JsonResponse({"message":"Success"}, status=200)
        except IntegrityError:
            return JsonResponse({"error":"Task with this ID already exists"}, status=409)
    
    return JsonResponse({"error":"Resource does not exist"}, status=404)

@csrf_exempt
def task_id(request, id):
    if request.method == "GET":
        print(id)
        try:
            task = Task.objects.get(id=id)
            tasks_list = convert_Task_to_JSON(task)
            return JsonResponse(tasks_list, safe=False, status=200)
        except Task.DoesNotExist:
            return JsonResponse({"error":"ID Not Found"}, status=404)
    
    if request.method == "PATCH":
        if not request.body:
            return JsonResponse({"error": "No JSON body provided"}, status=400)
        
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        task = Task.objects.get(id=id)
        if body.get("title"):
            task.title = body.get("title")
        if body.get("description"):
            task.description = body.get("description")
        if body.get("priority"):
            task.priority = int(body.get("priority"))
        if body.get("due_date"):
            due_date = body.get("due_date")
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
            task.due_date = due_date
        if body.get("user"):
            task.user = body.get("user")
        task.save()
        return JsonResponse({"message": "Success"}, status=200)

    if request.method == "POST":
        if not request.body:
            return JsonResponse({"error": "No JSON body provided"}, status=400)

        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        
        title, description, priority, due_date, user = body.get("title"), body.get("description"), body.get("priority"), body.get("due_date"), body.get("user")
        if title is None or description is None or priority is None or due_date is None or user is None:
            return JsonResponse({"error":"Missing or invalid input"}, status=400)
        
        priority = int(priority)
        due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        try:
            Task.objects.create(id=id, title=title, description=description, priority=priority, due_date=due_date, user=user, completed=False)
            return JsonResponse({"message":"Success"}, status=200)
        except IntegrityError:
            return JsonResponse({"error":"Task with this ID already exists"}, status=409)
    
    if request.method == "DELETE":
        try:
            task = Task.objects.get(id=id)
            task.delete()
            return JsonResponse({"message":"Success"}, status=200)
        except Task.DoesNotExist:
            return JsonResponse({"error":"ID Not Found"}, status=404)
    
    return JsonResponse({"error":"Resource does not exist"}, status=404)