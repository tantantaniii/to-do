from django.http import JsonResponse
from .models import *

from django.http import HttpResponse, HttpRequest, Http404

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control, never_cache
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_http_methods
from django.core import serializers
import json

@cache_control (
    private=True,
    max_age =  150*60,
    no_cache = True,
    no_site = False
)
def task_list(request: HttpRequest):
    if request.method == 'GET':
        tasks = Task.objects.all()
        tasks_list = []

        for task in tasks:
            tags = task.tag.all()
            tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]

            tasks_list.append(preparate_data(task, tags_list))

        return JsonResponse(tasks_list, safe=False)

@cache_control (
    private=True,
    max_age = 43200*60,
    no_cache = True,
    no_site = False
)
def task_detail(request: HttpRequest, task_id: int):
    if request.method == 'GET':
        # try:
            task = Task.objects.get(id=task_id)
            
            tags = task.tag.all()
            tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]
            
            task_dict = {
                "id": task.id,
                "title": task.title,
                "complition": task.complition,
                "tags": tags_list
            }
            
            return JsonResponse(task_dict)
        # except Task.DoesNotExist:
        #     raise Http404("Task not found")


@cache_control (
    private = True,
    max_age = 150*60,
    no_cache = True,
    no_site = False
)    
def task_list_create(request: HttpRequest):
    if request.method == 'GET':
        tasks = Task.objects.all()
        tasks_list = []
        for task in tasks:
            tags = task.tag.all()
            tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]
            tasks_list.append(preparate_data(task, tags_list))
        return JsonResponse(tasks_list, safe=False)
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        task = Task.objects.create(
            title=data['title'],
            complition=data.get('complition', False)
        )
        if 'tags' in data:
            tags = Tag.objects.filter(id__in=data['tags'])
            task.tag.set(tags)
        
        tags = task.tag.all()
        tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]
        response_data = preparate_data(task, tags_list)
        response_data['_links'] = {
            'self': {
                'type': 'GET',
                'url': f'{request.build_absolute_uri("/")}tasks/{task.id}/'
            }
        }
        return JsonResponse(response_data, status=201)

@cache_control(
    private = True,
    max_age = 720 * 60,  # 12 часов
    no_cache = False,
    no_site = False
)
@csrf_exempt
@require_http_methods(["GET", "DELETE", "PATCH"])
def task_detail_delete_update(request: HttpRequest, task_id: int):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)
    
    if request.method == 'GET':
        tags = task.tag.all()
        tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]
        task_dict = preparate_data(task, tags_list)
        return JsonResponse(task_dict)
    
    elif request.method == 'DELETE':
        task.delete()
        return JsonResponse({"message": "Task deleted successfully"}, status=204)
    
    elif request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            
            # Обновляем поля задачи
            if 'title' in data:
                task.title = data['title']
            if 'complition' in data:
                task.complition = data['complition']
            
            # Обновляем теги, если они переданы
            if 'tags' in data:
                tags = Tag.objects.filter(id__in=data['tags'])
                task.tag.set(tags)
            
            task.save()
            
            tags = task.tag.all()
            tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]
            response_data = preparate_data(task, tags_list)
            
            return JsonResponse(response_data)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@cache_control(
    private = True,
    max_age = 43200 * 60,  
    no_cache = False,
    no_site = False
)
@csrf_exempt
@require_http_methods(["GET", "DELETE", "PATCH"])
def tag_detail_delete_update(request: HttpRequest, tag_id: int):
    try:
        tag = Tag.objects.get(id=tag_id)
    except Tag.DoesNotExist:
        return JsonResponse({"error": "Tag not found"}, status=404)
    
    if request.method == 'GET':
        tag_dict = {
            "id": tag.id,
            "name": tag.name
        }
        return JsonResponse(tag_dict)
    
    elif request.method == 'DELETE':
        tag.delete()
        return JsonResponse({"message": "Tag deleted successfully"}, status=204)
    
    elif request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            
            if 'name' in data:
                tag.name = data['name']
                tag.save()
            
            return JsonResponse({
                "id": tag.id,
                "name": tag.name
            })
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
@cache_control(
    private = True,
    max_age = 1440 * 60, 
    no_cache = True,
    no_site = False
)
@csrf_exempt
@require_http_methods(["GET", "POST"])
def tag_list_create(request: HttpRequest):
    if request.method == 'GET':
        tags = Tag.objects.all()
        tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]
        return JsonResponse(tags_list, safe=False)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            if not data.get('name'):
                return JsonResponse({"error": "Name field is required"}, status=400)
                
            tag = Tag.objects.create(name=data['name'])
            
            response_data = {
                "id": tag.id,
                "name": tag.name,
                "_links": {
                    'self': {
                        'type': 'GET',
                        'url': f'{request.build_absolute_uri("/")}tags/{tag.id}/'
                    }
                }
            }
            return JsonResponse(response_data, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
def get_tasks_completed(request: HttpRequest):
    if request.method == 'GET':
        tasks = Task.objects.filter(complition=True)
        tasks_list = []

        for task in tasks:
            tags = task.tag.all()
            tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]

            tasks_list.append(preparate_data(task, tags_list))

        return JsonResponse(tasks_list, safe=False)

@cache_control (
    private=True,
    max_age = 150*60,
    no_cache = True,
    no_site = False
)
def get_tasks_uncompleted(request: HttpRequest):    
    if request.method == 'GET':
        tasks = Task.objects.filter(complition=False)
        tasks_list = []

        for task in tasks:
            tags = task.tag.all()
            tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]

            tasks_list.append(preparate_data(task, tags_list))

        return JsonResponse(tasks_list, safe=False)

@cache_control (
    private=True,
    max_age = 150*60,
    no_cache = True,
    no_site = False
)
def tag_list_create(request: HttpRequest):
    if request.method == 'GET':
        tags = Tag.objects.all()
        tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]
        return JsonResponse(tags_list, safe=False)

@cache_control (
    private=True,
    max_age = 150*60,
    no_cache = True,
    no_site = False
)
def tag_detail(request: HttpRequest, tag_id: int):
    if request.method == 'GET':
            tag = Tag.objects.get(id=tag_id)
            tag_dict = {
                "id": tag.id,
                "name": tag.name
            }
            return JsonResponse(tag_dict)

@cache_control (
    private=True,
    max_age = 150*60,
    no_cache = True,
    no_site = False
)
def task_via_tag_id(request: HttpRequest, tag_id: int):
    if request.method == 'GET':
        tasks = Task.objects.filter(tag=tag_id)
        tasks_list = []
        for task in tasks:
            tags = task.tag.all()
            tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]
            tasks_list.append(preparate_data(task, tags_list))

        return JsonResponse(tasks_list, safe=False)

@cache_control (
    private=True,
    max_age = 150*60,
    no_cache = True,
    no_site = False
)
def task_via_tag_id_uncompleted(request: HttpRequest, tag_id: int):
    if request.method == 'GET':
        tasks = Task.objects.filter(tag=tag_id, complition=False)
        tasks_list = []
        for task in tasks:
            tags = task.tag.all()
            tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]
            tasks_list.append(preparate_data(task, tags_list))

        return JsonResponse(tasks_list, safe=False)

@cache_control (
    private=True,
    max_age = 150*60,
    no_cache = True,
    no_site = False
)    
def task_via_tag_id_completed(request: HttpRequest, tag_id: int):
    if request.method == 'GET':
        tasks = Task.objects.filter(tag=tag_id, complition=True)
        tasks_list = []
        for task in tasks:
            tags = task.tag.all()
            tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]
            tasks_list.append(preparate_data(task, tags_list))

        return JsonResponse(tasks_list, safe=False)
        

def preparate_data(task_data: Task, tag_data: list[Tag]):
            
        task_dict = {
            "id": task_data.id,
            "title": task_data.title,
            "complition": task_data.complition,
            "tags": tag_data
        }
        return task_dict
                
#@never_cache
#def delete_tag(request: HttpRequest, tag_id: int):
#    tag = Tag.objects.filter(id=tag_id)
#    if tag:
#        tag.delete()
#        return JsonResponse("Тэг удален")
#    return Http404("Tag not found")

#@never_cache
#def delete_task(request: HttpRequest, task_id: int):
#    task = Task.objects.filter(id=task_id)
#    if task:
#        task.delete()
#        return HttpResponse("Задачка удалена")
#    return HttpResponse("Task not found")


# @csrf_exempt
# def task_create(request: HttpResponse):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         # task = Task.objects.create(
#         #     title=data["title"]
#         # )
#         # task.save()
#never_cache
#@csrf_exempt
#def task_create(request: HttpRequest):
#    if request.method == 'POST':
#        data = json.loads(request.body)

#       task = Task.objects.create(
#            title=data['title'],
#            complition=data.get('complition', False)
#        )
#
#        if 'tags' in data:
#           tags = Tag.objects.filter(id__in=data['tags'])
#            task.tag.set(tags)
#
#        tags = task.tag.all()
#        tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]
#        
#        response_data = preparate_data(task, tags_list)
#       
#        response_data['_links'] = {
#            'self': {
#                'type': 'GET',
#                'url': f'{request.build_absolute_uri("/")}tasks/{task.id}/'
#            }
#       }
#        
#        return JsonResponse(response_data, status=201)
    



# def tes_post(request):
#     print(request.body)