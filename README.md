Task Manager REST API

Task Manager application built using Python, Flask, MySQL, HTML, CSS, and JavaScript. It allows users to create, view, update, complete, and delete tasks through a web interface backed by REST API endpoints.

Features

- Create tasks with a title and optional description
- Retrieve and display saved tasks
- Edit task titles and descriptions
- Mark tasks as completed or pending
- Delete tasks
- Validate input and handle API errors
- Store task information in MySQL
- Provide a lightweight web interface

Technology Stack

- Backend: Python, Flask
- Database: MySQL
- Frontend: HTML, CSS, JavaScript
- API testing: Postman
- Automated testing: Pytest

Database Schema

Database: "task_manager_db"

Table: "tasks"

Column| Type| Description
"id"| INT| Auto-increment primary key
"title"| VARCHAR(150)| Required task title
"description"| TEXT| Optional task description
"completed"| TINYINT(1)| Task status: 0 = Pending, 1 = Completed
"created_at"| TIMESTAMP| Task creation timestamp

See ""schema.sql"" (schema.sql) for the SQL setup and ""DATABASE_SCHEMA.md"" (DATABASE_SCHEMA.md) for schema documentation.

API Endpoints

Base URL during local development: "http://127.0.0.1:5000"

Method| Endpoint| Purpose
GET| "/"| Check whether the API is running
GET| "/db-check"| Check database connectivity
GET| "/tasks"| Retrieve tasks
POST| "/tasks"| Create a task
PUT| "/tasks/<task_id>"| Update task details or status
DELETE| "/tasks/<task_id>"| Delete a task
GET| "/ui"| Open the web interface

Example: Create a task

Request: "POST /tasks"

{
  "title": "Learn Flask",
  "description": "Practice REST API development"
}

Use "Content-Type: application/json" when sending JSON request bodies.

Setup and Installation

Prerequisites

- Python
- MySQL Server
- Git (optional, for version control)

1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_PROJECT_FOLDER

Replace the placeholders with your actual repository URL and project folder name.

2. Create and activate a virtual environment

python -m venv .venv

On Windows:

.venv\Scripts\activate

3. Install dependencies

python -m pip install -r requirements.txt

4. Configure environment variables

Create a local ".env" file in the project root. Add your own MySQL connection details:

DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=task_manager_db

Do not upload ".env" or real database credentials to GitHub.

5. Create the database

Run "schema.sql" in your MySQL client to create the database and table.

6. Start the application

python app.py

Open the web interface at "http://127.0.0.1:5000/ui".

Testing

Run the automated tests with:

pytest

API endpoints can also be tested using Postman.

Future Improvements

- Add user authentication
- Add task filtering and sorting
- Improve task status indicators
- Deploy the application online

Author

Developed as a backend development portfolio project to practise REST API development, SQL database integration, input validation, error handling, and automated testing.
