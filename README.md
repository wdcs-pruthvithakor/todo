# Django ToDo Application

This is a simple ToDo application built using Django, a high-level Python web framework. The application allows users to manage their tasks, mark tasks as completed, edit tasks, and delete tasks. Users can sign up for an account, log in, and log out. The project follows the Model-View-Controller (MVC) architectural pattern provided by Django.

## Features

- **User authentication:** Users can sign up for a new account and log in using their username and password.
- **Task management:** Users can create, view, update, and delete tasks. Tasks include a title, description, completion status, and creation date.
- **Task filtering:** Users can filter tasks based on a search query, sort tasks by different criteria, and toggle the completion status of tasks.
- **User-friendly interface:** The application includes user-friendly forms, validation messages, and success messages for a better user experience.

## Technologies Used

- **Django:** The web framework used to build the application.
- **Python:** The programming language used for backend development.
- **HTML/CSS:** Frontend styling and structure.
- **Bootstrap:** Frontend framework for responsive and clean UI.
- **PostgreSQL:** The relational database used by Django for data storage.


## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/wdcs-pruthvithakor/todo.git
    cd todo
    ```

2. Create a virtual environment and install dependencies:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
    pip install -r requirements.txt
    ```

3. Configure the environment variables:

    Create a `.env` file in the project root and set the necessary environment variables:

    ```env
    POSTGREDB_NAME='library_management'
    POSTGREDB_USER='postgres'
    POSTGREDB_PASSWORD='postgres'
    POSTGREDB_HOST='127.0.0.1'
    POSTGREDB_PORT='5432'
    ```

    Update the values according to your PostgreSQL database configuration.

4. Run migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser account:

    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

7. **Open your web browser and go to http://localhost:8000/ to access the application.**


## Usage

1. **Create a new account:**

   Click on the "Sign Up" link, provide the required information, and create a new account.

2. **Log in:**

   Log in with your username and password.

3. **Manage Tasks:**

   Navigate to the "Tasks" section to manage your tasks. Create, edit, or delete tasks as needed.

4. **Log out:**

   Log out when you are done.

## Testing

The project uses the Django testing framework for writing and running tests. Before running tests, ensure you have set up the project and activated the virtual environment.

### Running Tests

To run the tests, use the following command:

```bash
python manage.py test
```

This will discover and run all the tests in the `tests` directory.

### Test Coverage

While writing tests, aim to achieve high test coverage to ensure the reliability of the application. Use tools like coverage.py to measure code coverage:

1. Install coverage.py:

    ```bash
    pip install coverage
    ```

2. Run tests with coverage:

    ```bash
    coverage run manage.py test
    ```

3. Generate coverage report:

    ```bash
    coverage report -m
    ```

This will display a detailed report indicating the percentage of code coverage.

### Mocking and Fixtures

Use Django's `TestCase` class to create fixtures and mock objects for testing. This ensures that tests are isolated and do not interfere with each other.
