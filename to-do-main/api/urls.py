from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='index'),
    path('tasks/', views.task_list_create, name='task_list_create'),
    path('tasks/<int:task_id>/', views.task_detail_delete_update, name='task_detail_delete_update'),
    path('tasks/completed/', views.get_tasks_completed, name='get_tasks_completed'),
    path('tasks/uncompleted/', views.get_tasks_uncompleted, name='get_tasks_uncompleted'),
    path('tags/', views.tag_list_create, name='tag_list'),
    path('tags/<int:tag_id>/', views.tag_detail_delete_update, name='tag_detail_delete_update'),
    path('tags/<int:tag_id>/tasks/', views.task_via_tag_id, name='task_via_tag_id'),
    path('tags/<int:tag_id>/tasks/completed/', views.task_via_tag_id_completed, name='task_via_tag_id_completed'),
    path('tags/<int:tag_id>/tasks/uncompleted/', views.task_via_tag_id_uncompleted, name='task_via_tag_id_uncompleted'),
]