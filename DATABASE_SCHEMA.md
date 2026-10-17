Database Schema

Database Name

"task_manager_db"

Table: "tasks"

Stores task details, completion status, and creation timestamp.

Column| Data Type| Constraints / Default
"id"| INT| Primary Key, AUTO_INCREMENT, NOT NULL
"title"| VARCHAR(150)| NOT NULL
"description"| TEXT| NULL allowed
"completed"| TINYINT(1)| NOT NULL, DEFAULT 0
"created_at"| TIMESTAMP| DEFAULT CURRENT_TIMESTAMP

Column Details

- id: Unique identifier for each task.
- title: Required task title, up to 150 characters.
- description: Optional additional information about the task.
- completed: Stores task status. "0" means Pending; "1" means Completed.
- created_at: Records when the task was created, using the database's current timestamp by default.

Relationships

The current schema contains one table and has no foreign-key relationships.

Database Operations

The Flask REST API performs CRUD operations on the "tasks" table:

- Create a task
- Retrieve tasks
- Update task details and completion status
- Delete a task
