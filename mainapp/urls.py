"""FamilyNotice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', LoginView.as_view(template_name = 'mainapp/login.html') , name = 'login'),
    path('logout/', LogoutView.as_view() , name = 'logout'),
    path('todolists/', views.todolist , name = 'todolists'),
    path('tasks/<int:List_id>/', views.tasks , name = 'tasks'),
    path('lists.json', views.lists_json, name="List of lists"),
    path('createList/', views.create_list, name="create list"),
    path('completed.json', views.complete_status, name="complete status"),
    path('register/', views.register, name="register"),
    path('mealplanner/', views.meal_planner, name="meal planner"),
    path('addmeal/<slug:meal>', views.addmeal, name="add meal"),
    path('addmeal2', views.addmeal2, name="add meal 2"),
    path('deleteMeal.json', views.deleteMeal, name="delete meal"),
    path('chooseFamily/', views.choose_family, name="choose family"),
    path('createFamily/', views.create_family, name="create family"),
    path('joinFamily/<int:Fam_id>/', views.join_family, name="join family"),
    path('leave_family/<int:Fam>/', views.leave_family, name="leave family"),
    path('searchKey/', views.search_key, name="search key"),
    path('current_members/', views.current_members, name="current members"),
    path('delete_list/<int:List_id>/', views.delete_list, name='delete list'),
    path('delete_task.json', views.delete_task, name='delete task'),
]
