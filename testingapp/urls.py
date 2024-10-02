from django.urls import path
from testingapp.views import *

urlpatterns=[
    path('register/',Register.as_view(),name='register'),
    path('login/',Login.as_view(),name="login"),
    path('task_view',TaskView.as_view(),name="task_view"),
    path('create_task',TaskCreateView.as_view(),name="create_task"),
    path('task_update/<int:pk>/',TaskUpdateView.as_view(),name="task_update"),
    path('task_delete/<int:pk>/',TaskDeleteView.as_view(),name="task_delete"),
    path('task_complete/<int:pk>/',TaskComplete.as_view(),name="task_complete"),
        
    
]