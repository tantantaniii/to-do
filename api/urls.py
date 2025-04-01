from django.urls import path
from . import views

urlpatterns = [
    # path('tasks/', views.task_list, name='task_list'),
     path('', views.task_list, name ='index'),
     path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
     path('tasks/completed/', views.get_tasks_completed, name='get_tasks_completed'),
     path('tasks/uncompleted/', views.get_tasks_uncompleted, name='get_tasks_uncompleted'),
     path('tags/', views.tag_list, name='tag_list'),
     path('tags/<int:tag_id>/', views.tag_detail, name='tag_detail'),
     path('tags/<int:tag_id>/tasks', views.task_via_tag_id, name='task_via_tag_id'),
     path('tags/<int:tag_id>/tasks/completed', views.task_via_tag_id_completed, name='task_via_tag_id_uncompleted'),
     path('tags/<int:tag_id>/tasks/uncompleted', views.task_via_tag_id_uncompleted, name='task_via_tag_id_uncompleted'),
     path('tags/delete/<int:tag_id>', views.delete_tag),
     path('tasks/delete/<int:task_id>', views.delete_task),
     path("tasks/create/", views.task_create),
    #  path("test/", views.tes_post)
]