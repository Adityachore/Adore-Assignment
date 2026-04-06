"""
QUICK API REFERENCE - Questions 7-9
===================================
"""

═══════════════════════════════════════════════════════════════════════════════
QUESTION 7: Task Relationship Endpoint
═══════════════════════════════════════════════════════════════════════════════

ENDPOINT:  GET /tasks/question7
PARAMETERS: id1 (int), id2 (int)

CURL EXAMPLE:
─────────────────────────────────────────────────────────────────────────────
curl -X GET "http://localhost:8000/tasks/question7?id1=3&id2=1"

PYTHON EXAMPLE:
─────────────────────────────────────────────────────────────────────────────
import requests

response = requests.get(
    "http://localhost:8000/tasks/question7",
    params={"id1": 3, "id2": 1}
)
print(response.json())

RESPONSES:
─────────────────────────────────────────────────────────────────────────────
✓ Task 3 is a subtask of Task 1
✓ Task 1 is a subtask of Task 3
✓ NONE


═══════════════════════════════════════════════════════════════════════════════
QUESTION 8: Date Range Query Endpoint
═══════════════════════════════════════════════════════════════════════════════

ENDPOINT 1: GET /tasks/question8/
(Database agnostic ORM approach - RECOMMENDED)

CURL EXAMPLE:
─────────────────────────────────────────────────────────────────────────────
curl -X GET "http://localhost:8000/tasks/question8/"

PYTHON EXAMPLE:
─────────────────────────────────────────────────────────────────────────────
import requests

response = requests.get("http://localhost:8000/tasks/question8/")
data = response.json()
print(f"Found {data['count']} tasks")
print(f"Filters applied: {data['filters_applied']}")

RESPONSE STRUCTURE:
─────────────────────────────────────────────────────────────────────────────
{
  "status": "success",
  "count": 5,
  "date_range": {
    "start": "2024-08-26",
    "end": "2024-09-09"
  },
  "filters_applied": [
    "created_between_26aug_9sep_2024",
    "exclude_completed_tasks",
    "exclude_sunday_created"
  ],
  "tasks": [
    {
      "id": 1,
      "name": "Task 1",
      "created_at": "2024-08-27T10:00:00",
      "priority": 1,
      "status": "pending"
    },
    ...
  ]
}


ENDPOINT 2: GET /tasks/question8/raw-sql
(Raw SQL approach - shows database-specific implementation)

CURL EXAMPLE:
─────────────────────────────────────────────────────────────────────────────
curl -X GET "http://localhost:8000/tasks/question8/raw-sql"

PYTHON EXAMPLE:
─────────────────────────────────────────────────────────────────────────────
import requests

response = requests.get("http://localhost:8000/tasks/question8/raw-sql")
data = response.json()
print(f"Database type: {data['database_type']}")
print(f"Found {data['count']} tasks")


═══════════════════════════════════════════════════════════════════════════════
QUESTION 9: Asynchronous Task Execution Endpoint
═══════════════════════════════════════════════════════════════════════════════

ENDPOINT:  POST /tasks/question9/{worker_threads}
PARAMETERS: worker_threads (int, path parameter)

CURL EXAMPLE:
─────────────────────────────────────────────────────────────────────────────
# Execute with 4 worker threads
curl -X POST "http://localhost:8000/tasks/question9/4"

# Execute with 2 worker threads
curl -X POST "http://localhost:8000/tasks/question9/2"


PYTHON EXAMPLE:
─────────────────────────────────────────────────────────────────────────────
import requests
import json

# Execute tasks with 4 workers
response = requests.post("http://localhost:8000/tasks/question9/4")
data = response.json()

# Print summary
summary = data['execution_details']['summary']
print(f"Total tasks: {summary['total_tasks']}")
print(f"Completed: {summary['completed_tasks']}")
print(f"Failed: {summary['failed_tasks']}")
print(f"Execution time: {summary['total_execution_time']:.2f}s")
print(f"Workers used: {summary['worker_threads']}")

# Access detailed logs
logs = data['execution_details']['execution_log']
for log in logs:
    if log['status'] == 'completed':
        print(f"Task {log['task_id']}: {log['actual_duration']:.2f}s")


RESPONSE STRUCTURE:
─────────────────────────────────────────────────────────────────────────────
{
  "status": "success",
  "execution_details": {
    "status": "completed",
    "summary": {
      "total_tasks": 4,
      "completed_tasks": 4,
      "failed_tasks": 0,
      "worker_threads": 4,
      "total_execution_time": 3.05
    },
    "execution_log": [
      {
        "task_id": 1,
        "task_name": "Task 1",
        "status": "completed",
        "scheduled_duration": 1.0,
        "actual_duration": 1.001,
        "priority": 1,
        "timestamp": "2024-04-05T10:30:45.123456"
      },
      {
        "task_id": 2,
        "task_name": "Task 2",
        "status": "completed",
        "scheduled_duration": 2.0,
        "actual_duration": 2.003,
        "priority": 1,
        "timestamp": "2024-04-05T10:30:45.500000"
      },
      ...
    ]
  }
}


═══════════════════════════════════════════════════════════════════════════════
TESTING WITH POSTMAN
═══════════════════════════════════════════════════════════════════════════════

1. Import the following requests into Postman:

Question 7:
  GET http://localhost:8000/tasks/question7?id1=3&id2=1

Question 8:
  GET http://localhost:8000/tasks/question8/
  GET http://localhost:8000/tasks/question8/raw-sql

Question 9:
  POST http://localhost:8000/tasks/question9/1
  POST http://localhost:8000/tasks/question9/2
  POST http://localhost:8000/tasks/question9/4
  POST http://localhost:8000/tasks/question9/8


═══════════════════════════════════════════════════════════════════════════════
ERROR HANDLING
═══════════════════════════════════════════════════════════════════════════════

Question 7:
- Returns "NONE" if no relationship found
- No error cases (function is robust)

Question 8:
- Returns empty task list if no matches found
- Works with any database type

Question 9:
- Returns 400 error if worker_threads <= 0
- Returns 404 error if no tasks found
- Returns detailed error in execution_log if task fails

Example Error Response (Q9):
{
  "detail": "worker_threads must be greater than 0"
}


═══════════════════════════════════════════════════════════════════════════════
SWAGGER UI DOCUMENTATION
═══════════════════════════════════════════════════════════════════════════════

Access interactive API documentation:
→ http://localhost:8000/docs

This provides:
✓ Visual endpoint documentation
✓ Try-it-out functionality
✓ Parameter validation
✓ Response examples
✓ Error documentation


═══════════════════════════════════════════════════════════════════════════════
NODEJS/JAVASCRIPT EXAMPLES
═══════════════════════════════════════════════════════════════════════════════

Question 7:
─────────────────────────────────────────────────────────────────────────────
const response = await fetch('http://localhost:8000/tasks/question7?id1=3&id2=1');
const data = await response.json();
console.log(data); // "Task 3 is a subtask of Task 1"


Question 8:
─────────────────────────────────────────────────────────────────────────────
const response = await fetch('http://localhost:8000/tasks/question8/');
const data = await response.json();
console.log(`Found ${data.count} tasks between ${data.date_range.start} and ${data.date_range.end}`);


Question 9:
─────────────────────────────────────────────────────────────────────────────
const response = await fetch('http://localhost:8000/tasks/question9/4', {
  method: 'POST'
});
const data = await response.json();
const summary = data.execution_details.summary;
console.log(`Execution time: ${summary.total_execution_time.toFixed(2)}s`);
console.log(`Completed: ${summary.completed_tasks}/${summary.total_tasks}`);


═══════════════════════════════════════════════════════════════════════════════
PERFORMANCE BENCHMARKS
═══════════════════════════════════════════════════════════════════════════════

For 4 tasks with durations: 10, 20, 30, 10 (total = 70 seconds = 7 seconds actual)

Workers: 1    → Execution time: ~7.00s
Workers: 2    → Execution time: ~4.00s
Workers: 4    → Execution time: ~3.00s
Workers: 8    → Execution time: ~3.00s (no improvement beyond task count)

KEY INSIGHT: Execution time ≈ (total_duration / worker_count)
Up to the number of tasks available.
"""
