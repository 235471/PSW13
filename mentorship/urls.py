from django.urls import path
from . import views

urlpatterns = [
    path('', views.mentorship, name='mentorship'),
    path('meeting/', views.meeting, name='meeting'),
    path('auth/', views.auth, name="auth_mentee"),
    path('schedule_date/', views.available_dates, name='available_dates'),
    path('schedule_meeting/', views.schedule_meeting, name='schedule_meeting'),
    path('mentee_tasks/', views.mentee_tasks, name='mentee_tasks'),
    path('task/<int:id>', views.task, name='task'),
    path('upload/<int:id>', views.upload, name='upload'),
    path('task_status/<int:id>', views.task_status, name='task_status'),
    path('mentee_logout/', views.mentee_logout, name='mentee_logout'), 
]
