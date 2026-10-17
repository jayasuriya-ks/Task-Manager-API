const taskForm = document.getElementById("task-form");
const taskList = document.getElementById("task-list");
const message = document.getElementById("message");

console.log("taskForm:", taskForm);
console.log("taskList:", taskList);
console.log("message:", message);

async function loadTasks() {
    try {
        const response = await fetch("/tasks");

        if (!response.ok) {
            throw new Error("Could not load tasks");
        }

        const data = await response.json();
        const tasks = data.tasks;
        taskList.innerHTML = "";

        console.log("Task received:", tasks);

        tasks.forEach(task => {
            const li = document.createElement("li");

            const title = document.createElement("strong");
            title.textContent = task.title;

            const description = document.createElement("p");
            description.textContent = task.description || "No description";

            const status = document.createElement("p");
            status.textContent = task.completed ? "Completed" : "Pending";

const editButton = document.createElement("button");
editButton.textContent = "Edit";
editButton.style.marginRight = "8px";

editButton.addEventListener("click", async function () {
    const newTitle = prompt("Edit task title:", task.title);

    if (newTitle === null) {
        return;
    }

    const trimmedTitle = newTitle.trim();

    if (!trimmedTitle) {
        alert("Task title cannot be empty.");
        return;
    }

    const newDescription = prompt(
        "Edit task description:",
        task.description || ""
    );

    if (newDescription === null) {
        return;
    }

    try {
        const response = await fetch(`/tasks/${task.id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: trimmedTitle,
                description: newDescription.trim(),
                completed: Boolean(task.completed)
            })
        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.error || "Could not edit task.");
            return;
        }

        await loadTasks();
    } catch (error) {
        console.error("Edit task error:", error);
        alert("Unable to edit task.");
    }
});



const completeButton = document.createElement("button");
completeButton.textContent = task.completed
    ? "Mark as Pending"
    : "Mark as Completed";

completeButton.style.marginRight = "8px";

completeButton.addEventListener("click", async function () {
    try {
        const response = await fetch(`/tasks/${task.id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: task.title,
                description: task.description || "",
                completed: !task.completed
            })
        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.error || "Could not update task.");
            return;
        }

        await loadTasks();
    } catch (error) {
        console.error("Update task error:", error);
        alert("Unable to update task.");
    }
});



            const deleteButton = document.createElement("button");
deleteButton.textContent = "Delete";
deleteButton.style.backgroundColor = "red";

deleteButton.addEventListener("click", async function () {
    const confirmed = confirm("Are you sure you want to delete this task?");

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(`/tasks/${task.id}`, {
            method: "DELETE"
        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.error || "Could not delete task.");
            return;
        }

        await loadTasks();
    } catch (error) {
        console.error("Delete task error:", error);
        alert("Unable to delete task.");
    }
});

li.append(title, description, status, editButton, completeButton, deleteButton);
taskList.appendChild(li);


        });

        message.textContent = "";
    } catch (error) {
        console.error("Load tasks error:", error);
        message.textContent = "Unable to load tasks. Please try again.";
    }
}

taskForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const title = document.getElementById("task-title").value.trim();
    const description = document
        .getElementById("task-description").value.trim();

    if (!title) {
        message.textContent = "Please enter a task title.";
        return;
    }

    try {
        const response = await fetch("/tasks", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: title,
                description: description
            })
        });

        const result = await response.json();

        if (!response.ok) {
            message.textContent = result.error || "Could not add task.";
            return;
        }

        taskForm.reset();
        message.textContent = "Task added successfully!";
        await loadTasks();
    } catch (error) {
        message.textContent = "Unable to connect to the API.";
    }
});

loadTasks();

