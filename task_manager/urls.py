from django.urls import path
from django.views.generic.base import RedirectView
from .views import (
    TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView,
    CustomSignupView, CustomLoginView, CustomLogoutView, TaskToggleCompleteView
)

urlpatterns = [
    path('', RedirectView.as_view(url='login/', permanent=True),name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', CustomSignupView.as_view(), name='signup'),
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('task/create/', TaskCreateView.as_view(), name='task_create'),
    path('task/update/<int:pk>/', TaskUpdateView.as_view(), name='task_update'),
    path('task/delete/<int:pk>/', TaskDeleteView.as_view(), name='task_delete'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/toggle_complete/<int:pk>/', TaskToggleCompleteView.as_view(), name='toggle_complete'),
]
