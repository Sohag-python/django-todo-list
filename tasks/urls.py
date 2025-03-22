from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task-list'),  # ✅ Ensure this exists
    path('task/<int:task_id>/', views.task_detail, name='task-detail'),
    path('task/create/', views.task_create, name='task-create'),
    path('task/delete/<int:task_id>/', views.task_delete, name='task-delete'),  # ✅ Ensure correct name
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
