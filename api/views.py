
from django.http import JsonResponse
from .models import *

from django.http import HttpResponse, HttpRequest, Http404

from django.views.decorators.csrf import csrf_exempt
import json
# class MyEncoder(DjangoJSONEncoder):
#     def default(self, o):
#         if isinstance(o, Q):
#             ...

# {
#     "id": 1,
#     "title": "TestTask1",
#     "complition": false,
#     tags: [
#         {
#             "id" 1,
#             "name": asdasd
#         }
#     ]
# }

def task_list(request: HttpRequest):
    # if request.method == 'GET':
    #     tasks = Task.objects.all()
    #     tasks_data = serializers.serialize('json', tasks)  
    #     # print(tasks_data) 
    #     # for task in tasks:
    #     #     pass
    #     return JsonResponse(tasks.values().first(), safe=False)
   
    # if request.method == 'GET':
    #     tasks = Task.objects.values('id', 'title', 'complition', 'tag')
    #     tasks_list = list(tasks)
    #     return JsonResponse(tasks_list, safe=False)
    if request.method == 'GET':
        tasks = Task.objects.all()
        tasks_list = []

        for task in tasks:
            tags = task.tag.all()
            tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]

            tasks_list.append(preparate_data(task, tags_list))

        return JsonResponse(tasks_list, safe=False)


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


    
def get_tasks_completed(request: HttpRequest):
    # if request.method == 'GET':
    #     tasks = Task.objects.all()
    #     tasks_data = serializers.serialize('json', tasks)  
    #     # print(tasks_data) 
    #     # for task in tasks:
    #     #     pass
    #     return JsonResponse(tasks.values().first(), safe=False)
   
    # if request.method == 'GET':
    #     tasks = Task.objects.values('id', 'title', 'complition', 'tag')
    #     tasks_list = list(tasks)
    #     return JsonResponse(tasks_list, safe=False)
    if request.method == 'GET':
        tasks = Task.objects.filter(complition=True)
        tasks_list = []

        for task in tasks:
            tags = task.tag.all()
            tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]

            tasks_list.append(preparate_data(task, tags_list))

        return JsonResponse(tasks_list, safe=False)


def get_tasks_uncompleted(request: HttpRequest):

    
    if request.method == 'GET':
        tasks = Task.objects.filter(complition=False)
        tasks_list = []

        for task in tasks:
            tags = task.tag.all()
            tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]

            tasks_list.append(preparate_data(task, tags_list))

        return JsonResponse(tasks_list, safe=False)

def tag_list(request: HttpRequest):
    if request.method == 'GET':
        # test = Task.objects.filter(tag=1)
        # print(test)
        tags = Tag.objects.all()
        tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]
        return JsonResponse(tags_list, safe=False)
    
def tag_detail(request: HttpRequest, tag_id: int):
    if request.method == 'GET':
            tag = Tag.objects.get(id=tag_id)
            tag_dict = {
                "id": tag.id,
                "name": tag.name
            }
            return JsonResponse(tag_dict)


#/tasks/?tags=1,2,3

def task_via_tag_id(request: HttpRequest, tag_id: int):
    if request.method == 'GET':
        tasks = Task.objects.filter(tag=tag_id)
        tasks_list = []
        for task in tasks:
            tags = task.tag.all()
            tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]
            tasks_list.append(preparate_data(task, tags_list))

        return JsonResponse(tasks_list, safe=False)
    
def task_via_tag_id_uncompleted(request: HttpRequest, tag_id: int):
    if request.method == 'GET':
        tasks = Task.objects.filter(tag=tag_id, complition=False)
        tasks_list = []
        for task in tasks:
            tags = task.tag.all()
            tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]
            tasks_list.append(preparate_data(task, tags_list))

        return JsonResponse(tasks_list, safe=False)
    
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
                

def delete_tag(request: HttpRequest, tag_id: int):
    tag = Tag.objects.filter(id=tag_id)
    if tag:
        tag.delete()
        return JsonResponse("Тэг удален")
    return Http404("Tag not found")

def delete_task(request: HttpRequest, task_id: int):
    task = Task.objects.filter(id=task_id)
    if task:
        task.delete()
        return HttpResponse("Задачка удалена")
    return HttpResponse("Task not found")


# @csrf_exempt
# def task_create(request: HttpResponse):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         # task = Task.objects.create(
#         #     title=data["title"]
#         # )
#         # task.save()
@csrf_exempt
def task_create(request: HttpRequest):
    if request.method == 'POST':
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
    



# def tes_post(request):
#     print(request.body)