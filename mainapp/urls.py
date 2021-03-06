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
from . import viewsCal
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', LoginView.as_view(template_name = 'mainapp/login.html') , name = 'login'),
    path('logout/', LogoutView.as_view() , name = 'logout'),
    path('register/', views.register, name="register"),
    path('current_members/', views.current_members, name="current members"),

    ##List and Task Urls
    path('lists.json', views.lists_json, name="List of lists"),
    path('todolists/', views.todolist , name = 'todolists'),
    path('tasks/<int:List_id>/', views.tasks , name = 'tasks'),
    path('createList/', views.create_list, name="create list"),
    path('completed.json', views.complete_status, name="complete status"),
    path('delete_list/<int:List_id>/', views.delete_list, name='delete list'),
    path('delete_task.json', views.delete_task, name='delete task'),

    ##MealPlanner URLs
    path('mealplanner/', views.meal_planner, name="meal planner"),
    path('addmeal/<slug:meal>', views.addmeal, name="add meal"),
    path('addmeal2', views.addmeal2, name="add meal 2"),
    path('deleteMeal.json', views.deleteMeal, name="delete meal"),

    #Chore/Reward URLs
    path('addchore/', views.addchore, name="add chore"),
    path('addreward/', views.addreward, name="add reward"),
    path('claim', views.claim, name="claim"),
    path('delete_chore.json', views.delete_chore, name='delete chore'),
    path('delete_reward.json', views.delete_reward, name='delete reward'),
    path('chore_completed.json', views.chore_completed, name='chore completed'),
    path('chores/', views.chores, name='chores'),
    path('accept_claim/', views.accept_claim, name='accept claim'),

    ##Choose Family URLs
    path('chooseFamily/', views.choose_family, name="choose family"),
    path('createFamily/', views.create_family, name="create family"),
    path('joinFamily/<int:Fam_id>/', views.join_family, name="join family"),
    path('leave_family/<int:Fam>/', views.leave_family, name="leave family"),
    path('searchKey/', views.search_key, name="search key"),
    path('shareKey/', views.share_key, name="share key"),

    ##Chat URLs
    path('chat/', views.chat, name='chat'),
    path('addMessage/', views.add_message, name='add message'),

    ##Location URLs
    path('findFamily/', views.location, name='location'),
    path('findFamily2/', views.location_of_member, name='location of member'),

    #Calendar URLs
    path('calendar/', viewsCal.get_credentials, name='calendar'),
    path('SignOutGoogle/', viewsCal.SignOutGoogle, name='SignOutGoogle'),
    path('calendarAdd/', viewsCal.create_event, name='calendarAdd'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete '),
]
