# Task Tracker API

Users can create, update, complete, and design tasks. These tasks will have due dates and priority levels. Later I will add pagination and filtering.

## Features

### **GET /task**

Retrieves all tasks. Pagination may be added in the future.

**Query Parameters:**

- dueDate: Filter tasks by due date (YYYY-MM-DD)
- priority: Filter tasks by priority level (1 - 10)
- user: Filter tasks by user

**Responses:**

- 200 OK - Returns a list of tasks
- 400 BAD REQUEST - Invalid query parameters

### **GET /task/:id**

Retrieves a post with the given ID.

**Responses:**

- 200 OK - Returns task with given ID
- 404 NOT FOUND - ID not found

### **POST /task**

Creates a new task with name, priority level, due date, unique ID and user, and adds it to database. The data is passed in the JSON body.

**Request Body (JSON):**

```json
{
  "id": "integer", // Unique task ID
  "title": "string", // Task name
  "description": "string", // Task description
  "priority": "int", // Task priority (1 - 10)
  "dueDate": "string", // Due date in YYYY-MM-DD format
  "user": "string", // The user who created the task
  "completed": "boolean" // Whether the task is completed or not
}
```

**Responses:**

- 200 OK - Task successfully created
- 409 CONFLICT - ID already exists
- 400 BAD REQUEST - Missing or invalid input

### **PATCH /task/:id**

Updates an existing task with the data provided in the JSON request body.

**Responses:**

- 200 OK - Task successfully updated
- 404 NOT FOUND - ID not found
- 400 BAD REQUEST - Missing or invalid input

## **DELETE /task/:id**

Removes an existing task using the ID provided
**Responses:**

- 200 OK - Task successfully deleted
- 404 NOT FOUND - ID not found
- 400 BAD REQUEST - Invalid ID format
