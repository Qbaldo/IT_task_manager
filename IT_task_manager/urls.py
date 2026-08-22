"""
URL configuration for IT_task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from IT_task_manager.views import (position_list,
                                   worker_list,
                                   task_type_list,
                                   task_list,
                                   position_create,
                                   position_update,
                                   position_delete,
                                   worker_detail,
                                   worker_create,
                                   worker_update,
                                   worker_delete,
                                   task_type_create,
                                   task_type_update,
                                   task_type_delete,
                                   task_create,
                                   task_update,
                                   task_complete,
                                   task_detail,
                                   task_delete,
                                   index)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('positions/', position_list, name='position-list'),
    path('workers/', worker_list, name='worker-list'),
    path('tasks/', task_list, name='task-list'),
    path('task-type/', task_type_list, name='task-type-list'),
    path('position_create/', position_create, name='position-create'),
    path('position/<int:pk>/update/', position_update,
         name='position-update',),
    path('position/<int:pk>/delete', position_delete, name='position-delete'),
    path('workers/<int:pk>', worker_detail, name='worker-detail'),
    path('worker_create/', worker_create, name='worker-create'),
    path('worker/<int:pk>/update/', worker_update, name='worker-update'),
    path('workers/<int:pk>/delete/', worker_delete, name='worker-delete'),
    path('task_type_create/', task_type_create, name='task-type-create'),
    path('task-type/<int:pk>/update/', task_type_update,
         name='task-type-update'),
    path('task_type_delete/<int:pk>/delete/', task_type_delete,
         name='task-type-delete'),
    path('task_create', task_create, name='task-create'),
    path('task/<int:pk>/update/', task_update, name='task-update'),
    path('task/<int:pk>/complete/', task_complete, name='task-complete'),
    path('task_detail/<int:pk>', task_detail, name='task-detail'),
    path('task_delete/<int:pk>/delete', task_delete, name='task-delete'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', index, name='home'),


]
