from django.contrib import messages
from django.shortcuts import redirect
from .models import Task

class TaskExistsMixin:
    """
    This mixin is used to check if the task exists and if not, redirect to the task list.
    """
    def task_exists(self, request, *args, **kwargs):
        """
        Check if a task exists for the given user and primary key. 
        :param request: The HTTP request object. 
        :param args: Variable length argument list. 
        :param kwargs: Arbitrary keyword arguments. 
        :return: The HTTP response object.
        """
        if not Task.objects.filter(pk=kwargs['pk'], user=self.request.user).exists():
            messages.error(request, 'Task not found.', extra_tags='bg-danger')
            return redirect('task_list')
        return super().get(request, *args, **kwargs)
