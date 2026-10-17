from flask import Flask, jsonify, request,render_template
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host= os.getenv("DB_HOST"),
        user= os.getenv("DB_USER"),
        password= os.getenv("DB_PASSWORD"),
        database= os.getenv("DB_NAME")
    )


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Task Manager API is running!"
    })

@app.route("/ui")
def home_page():
    return render_template("index.html")

@app.route("/db-check", methods=["GET"])
def db_check():
    connection = None

    try:
        connection = get_db_connection()

        if connection.is_connected():
            return jsonify({
                "message": "MySQL connection successful!"
            }), 200

    except Error:
        app.logger.exception("Database connection failed")
        return jsonify({
            "error": "Could not connect to the database"
        }), 500

    finally:
        if connection and connection.is_connected():
            connection.close()



@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    title = data.get("title")
    description = data.get("description", "")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Title is required"}), 400

    if len(title.strip()) > 150:
        return jsonify({"error": "Title must be 150 characters or fewer"}), 400

    if not isinstance(description, str):
        return jsonify({"error": "Description must be a string"}), 400

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        sql = """
            INSERT INTO tasks (title, description)
            VALUES (%s, %s)
        """
        cursor.execute(sql, (title.strip(), description))
        connection.commit()

        task_id = cursor.lastrowid

        return jsonify({
            "message": "Task created successfully",
            "task": {
                "id": task_id,
                "title": title.strip(),
                "description": description,
                "completed": False
            }
        }), 201

    except Error:
        app.logger.exception("Failed to create task")
        return jsonify({"error": "Database operation failed"}), 500

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()



@app.route("/tasks", methods=["GET"])
def get_tasks():
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, title, description, completed, created_at
            FROM tasks
            ORDER BY id DESC
        """)

        tasks = cursor.fetchall()

        for task in tasks:
            if task["created_at"] is not None:
                task["created_at"] = task["created_at"].isoformat()

        return jsonify({"tasks": tasks}), 200

    except Error:
        app.logger.exception("Failed to retrieve tasks")
        return jsonify({"error": "Database operation failed"}), 500

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()



@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    connection = None
    cursor = None

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be JSON"}), 400

    title = data.get("title")
    description = data.get("description","")
    completed = data.get("completed", False)

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Title is required"}), 400

    if len(title.strip()) > 150:
        return jsonify({"error": "Title must be 150 characters or fewer"}), 400

    if description is not None and not isinstance(description, str):
        return jsonify({"error": "Description must be text"}), 400

    if not isinstance(completed, bool):
        return jsonify({"error": "Completed must be true or false"}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            UPDATE tasks
            SET title = %s, description = %s, completed = %s
            WHERE id = %s
            """,
            (title.strip(), description, completed, task_id)
        )

        if cursor.rowcount == 0:
            cursor.execute(
                "SELECT id FROM tasks WHERE id = %s",
                (task_id,)
            )
            if cursor.fetchone() is None:
                return jsonify({"error": "Task not found"}), 404

        connection.commit()

        return jsonify({
            "message": "Task updated successfully",
            "id": task_id,
            "title": title.strip(),
            "description": description,
            "completed": completed
        }), 200

    except Error:
        if connection is not None:
            connection.rollback()
        app.logger.exception("Failed to update task")
        return jsonify({"error": "Database operation failed"}), 500

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()



@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM tasks WHERE id = %s",
            (task_id,)
        )

        if cursor.rowcount == 0:
            return jsonify({"error": "Task not found"}), 404

        connection.commit()

        return jsonify({
            "message": "Task deleted successfully",
            "id": task_id
        }), 200

    except Error:
        if connection is not None:
            connection.rollback()

        app.logger.exception("Failed to update task")
        return jsonify({"error": "Database operation failed"}), 500

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    app.run(debug=True)



