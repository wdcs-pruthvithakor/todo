from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, FormView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q
from .models import Task
from .forms import TaskForm, CustomSignupForm, CustomLoginForm
from .mixins import TaskExistsMixin

class TaskListView(LoginRequiredMixin, ListView):
    """
    List view for tasks.
    """
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'
    paginate_by = 8
    ordering = ['title']
    
    def get_queryset(self):
        """
        Return the queryset after filtering based on the request parameters 'q', 'order_by', and 'dir'.
        """
        query = self.request.GET.get('q')
        order_by = self.request.GET.get('order_by', 'title')
        dir = self.request.GET.get('dir', 'asc')

        queryset = Task.objects.filter(user=self.request.user)

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        if order_by:
            if dir == 'asc':
                queryset = queryset.order_by(order_by)
            elif dir == 'desc':
                queryset = queryset.order_by(f'-{order_by}')

        return queryset

    def get_context_data(self, **kwargs):
        """
        Return the context data with additional order_by, dir, and search_query parameters.
        """
        context = super().get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', 'title')
        context['dir'] = self.request.GET.get('dir', 'asc')
        context['search_query'] = self.request.GET.get('q')
        return context

    
class TaskDetailView(LoginRequiredMixin, TaskExistsMixin, DetailView):
    """
    Detail view for tasks.
    """
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        """
        Return the queryset of Task objects filtered by the current user.
        """
        return Task.objects.filter(user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        """
        Get method to check if a task exists and return the result.
        Args:
            request: The request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The result of the task_exists method.
        """
        return self.task_exists(request, *args, **kwargs)

class TaskCreateView(LoginRequiredMixin, CreateView):
    """
    Create view for tasks.
    """
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task_list')
    
    def form_valid(self, form):
        """
        Check if the form is valid and return the response.
        :param form: the form to be validated
        :return: the response after the form validation
        """
        form.instance.user = self.request.user
        response = super().form_valid(form)
   
        messages.success(self.request, 'Task added successfully.', extra_tags='bg-success')

        return response

class TaskToggleCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = Task.objects.get(pk=pk, user=request.user)
        task.completed = not task.completed
        task.save()
        if task.completed:
            messages.success(request, f'Task completed successfully.', extra_tags='bg-success')
        else:
            messages.success(request, f'Task reopened successfully.', extra_tags='bg-success')
        return redirect(reverse_lazy('task_list'))

class TaskUpdateView(LoginRequiredMixin, TaskExistsMixin, UpdateView):
    """
    Update view for tasks.
    """
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        """
        Return the queryset of Task objects filtered by the current user.
        """
        return Task.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        """
        Get method to check if a task exists and return the result.
        Args:
            request: The request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The result of the task_exists method.
        """
        return self.task_exists(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Check if the form is valid and return the response.
        :param form: the form to be validated
        :return: the response after the form validation
        """
        
        response = super().form_valid(form)
        obj = self.get_object()
        messages.success(self.request, f'Task {obj.title} edited successfully.', extra_tags='bg-success')

        return response

class TaskDeleteView(LoginRequiredMixin, TaskExistsMixin, DeleteView):
    """
    Delete view for tasks.
    """
    model = Task
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        """
        Return the queryset of Task objects filtered by the current user.
        """
        return Task.objects.filter(user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        """
        Get method to check if a task exists and return the result.
        Args:
            request: The request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The result of the task_exists method.
        """
        return self.task_exists(request, *args, **kwargs)

    def get_success_url(self):
        """
        Return the success URL for the view. 
        """
        obj = self.get_object()
        messages.success(self.request, f'Task {obj.title} has been deleted successfully.', extra_tags='bg-success')
        return super().get_success_url()

class CustomSignupView(FormView):
    """
    View for signing up a user.
    """
    template_name = 'signup.html'
    form_class = CustomSignupForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """
        Validate the form and save the user's information. 

        Args:
            form: The form to be validated.

        Returns:
            The result of calling the parent class's form_valid method.
        """
        user = form.save()
        messages.success(self.request, 'Account created successfully.', extra_tags='bg-success')
        return super().form_valid(form)

class CustomLoginView(FormView):
    """
    View for logging in a user.
    """
    template_name = 'login.html'
    form_class = CustomLoginForm
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        """
        Method to handle the validation of a form.
        
        Args:
            form: The form to be validated.

        Returns:
            The result of calling the form_valid method of the superclass.
        """
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Logged in successfully.', extra_tags='bg-success')
        return super().form_valid(form)

class CustomLogoutView(View):
    """
    View for logging out a user.
    """
    
    def get(self, request, *args, **kwargs):
        """
        Perform a GET request, log out the user, display a success message, and redirect to the login page.
        
        :param request: the HTTP request object
        :param args: additional positional arguments
        :param kwargs: additional keyword arguments
        :return: a redirection to the 'login' page
        """
        logout(request)
        messages.success(request, 'Logged out successfully.', extra_tags='bg-success')
        return redirect('login')
