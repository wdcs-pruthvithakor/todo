# library/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task

class TaskAuthTests(TestCase):
    """
    Test the authentication views of the task manager app.
    """
    def setUp(self):
        """
        Set up the test environment by creating some test data including a user and a task.
        """
        # Create some test data
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.task = Task.objects.create(title='Test Task', description='Test Description', user=self.user)

    def test_sign_up_view(self):
        """
        Test the sign-up view by simulating a POST request with user data and checking the response and database state.
        """
        url = reverse('signup')
        data = {'username': 'newuser', 'email': 'WJqXc@example.com' , 'password': 'Userpass001', 'confirm_password': 'Userpass001'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful signup
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view(self):
        """
        Log in the user, test if login was successful, and assert query and response details.
        """
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Test if login was successful
        response = self.client.get(reverse('task_list'))
        self.assertQuerySetEqual(response.context['object_list'], [self.task])
        self.assertContains(response, 'Test Task')
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        """
        Test the logout view by logging in the user, then logging them out and checking the response.
        """
        # Log in the user
        self.client.login(username='testuser', password='testpass')
        # Log out the user
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after successful logout
        self.assertFalse(self.client.session.get('_auth_user_id'))
        
class TaskTests(TestCase):
    """
    Test the views of the task manager app.
    """

    def setUp(self):
        """
        Set up the test environment by creating a test user, logging in the user, and creating some test data.
        """
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Create some test data
        self.task = Task.objects.create(title='Test Task', description='Test Description', user=self.user)

    def test_task_list_view(self):
        """
        Test the task list view.
        """
        url = reverse('task_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['object_list'], [self.task])
        self.assertContains(response, 'Test Task')

    def test_task_create_view(self):
        """
        Test the task create view by posting data and checking the response and database.
        """
        url = reverse('task_create')
        data = {'title': 'New Task', 'user': self.user, 'description': 'Test Description'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_task_update_view(self):
        """
        Test the task update view by sending a POST request with updated task data.
        """
        url = reverse('task_update', args=[self.task.id])
        data = {'title': 'Updated Task', 'user': self.user, 'description': 'Test Description', 'completed': True}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.completed, True)

    def test_task_delete_view(self):
        """
        A test for the task_delete_view function. It generates a URL, sends a POST request to the URL using the client, checks that the response status code is 302, and ensures that the Task with the title 'Test Task' does not exist in the database.
        """
        url = reverse('task_delete', args=[self.task.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        self.assertFalse(Task.objects.filter(title='Test Task').exists())

    def test_task_detail_view(self):
        """
        A test for the task_detail_view function.
        """
        url = reverse('task_detail', args=[self.task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')
        
    def test_toggle_complete_view(self):
        """
        Test the toggle_complete_view function.
        """
        url = reverse('toggle_complete', args=[self.task.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        self.task.refresh_from_db()
        self.assertEqual(self.task.completed, True)
