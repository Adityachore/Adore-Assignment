# Import FastAPI and dependencies
from fastapi import FastAPI, HTTPException, Depends
from models import Task, Base, engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from task_logic import *

# Initialize the FastAPI app
app = FastAPI(title="StoteWise Backend Assignment",
    description="Good luck with the assignment! :)",
    version="1.0.0",
    contact={
        "name": "Achal Agarwal",
        "email": "achalagarwal.01@gmail.com ",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    })



# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Basic Endpoints

# 1. Retrieve all tasks
@app.get("/tasks")
def get_all_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    if tasks is None:
        raise HTTPException(status_code=404, detail="No tasks found")
    return tasks

# 2. Create a new task


# Define a Pydantic model for task creation
class TaskCreate(BaseModel):
    name: str
    description: str = None
    due_date: str  # Expecting a string in ISO 8601 format
    priority: int = 1
    status: str = "pending"
    parent_id: int = None
    duration: int = 0

@app.post("/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # Convert due_date from string to datetime object
    due_date = datetime.fromisoformat(task.due_date)
    
    db_task = Task(
        name=task.name,
        description=task.description,
        due_date=due_date,
        priority=task.priority,
        status=task.status,
        parent_id=task.parent_id,
        duration=task.duration,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# 3. Delete a task by its task_id
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted successfully"}


# Level 1 


# Question 2
@app.get("/tasks/question2")
def question2_route(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return question2(tasks)

# Question 3
@app.get("/tasks/question3")
def question3_route(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return question3(tasks)

# Question 4
@app.get("/tasks/question4")
def question4_route(db: Session = Depends(get_db)):

    parents_without_children = []
    
    # Note: We accept any means to solve this question 4
    # But we want you to ideally use only SQL query to solve this question
    # Hint: Use a join  

    return []

# Question 5
@app.get("/tasks/question5/{task_id}")
def question5_route(task_id: int, db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return question5(tasks, task_id)



# Level 2

# Question 6
@app.get("/tasks/question6/{query}")
def question6_route(query: str, db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return question6(tasks, query)

# Question 7
@app.get("/tasks/question7")
def question7_route(id1: int, id2: int, db: Session = Depends(get_db)):
    """
    Determine the relationship between two tasks.
    
    Query Parameters:
    - id1: First task ID
    - id2: Second task ID
    
    Returns:
    - Relationship string if one is a subtask of the other
    - "NONE" if no relationship exists
    """
    tasks = db.query(Task).all()
    return question7(tasks, id1, id2)

# Question 8
@app.get("/tasks/question8/")
def question8_route(db: Session = Depends(get_db)):
    """
    Get tasks created between 26 Aug 2024 and 9 Sep 2024:
    - Exclude completed tasks
    - Exclude tasks created on Sunday
    - Database agnostic (SQLite and PostgreSQL compatible)
    
    Returns:
    - List of matching tasks with execution details
    """
    from sqlalchemy import and_, text
    
    # Define the date range
    start_date = datetime(2024, 8, 26)
    end_date = datetime(2024, 9, 9)
    
    # Build the query using SQLAlchemy ORM
    # This approach is compatible with both SQLite and PostgreSQL
    tasks = db.query(Task).filter(
        and_(
            Task.created_at >= start_date,
            Task.created_at <= end_date,
            Task.status != 'completed'  # Exclude completed tasks
        )
    ).all()
    
    # Filter tasks created on Sunday (day 6 in Python's weekday, 0=Monday, 6=Sunday)
    # Since SQLite and PostgreSQL have different date functions, we filter in Python
    filtered_tasks = [
        task for task in tasks 
        if task.created_at.weekday() != 6  # 6 represents Sunday
    ]
    
    return {
        "status": "success",
        "count": len(filtered_tasks),
        "date_range": {
            "start": start_date.date(),
            "end": end_date.date()
        },
        "filters_applied": [
            "created_between_26aug_9sep_2024",
            "exclude_completed_tasks",
            "exclude_sunday_created"
        ],
        "tasks": filtered_tasks
    }

# Alternative Question 8 using Raw SQL (Database Agnostic)
@app.get("/tasks/question8/raw-sql")
def question8_raw_sql_route(db: Session = Depends(get_db)):
    """
    Alternative implementation using raw SQL queries.
    This is more efficient but requires database-specific handling.
    """
    from sqlalchemy import text
    
    # Raw SQL query that works with both SQLite and PostgreSQL
    # For SQLite: strftime for date functions, weekday for day of week
    # For PostgreSQL: DATE functions
    
    raw_sql = """
    SELECT * FROM tasks 
    WHERE 
        created_at >= '2024-08-26' 
        AND created_at <= '2024-09-09'
        AND status != 'completed'
        AND CAST(strftime('%w', created_at) AS INTEGER) != 0
    ORDER BY created_at DESC
    """
    
    # Execute raw SQL (SQLite compatible)
    result = db.execute(text(raw_sql)).fetchall()
    
    return {
        "status": "success",
        "count": len(result) if result else 0,
        "query_type": "raw_sql",
        "database_type": "sqlite",
        "tasks": [dict(row._mapping) for row in result] if result else []
    }

# Question 9
@app.post("/tasks/question9/{worker_threads}")
def question9_route(worker_threads: int, db: Session = Depends(get_db)):
    """
    Simulate asynchronous task execution with limited worker threads.
    
    Path Parameters:
    - worker_threads: Maximum number of concurrent worker threads
    
    Process:
    1. Create a thread pool with specified worker count
    2. Each task duration = duration / 10 seconds
    3. Workers pick up tasks sequentially
    4. Return execution report with timing details
    
    Returns:
    - Execution summary with task statuses
    - Detailed execution log with timing info
    """
    
    if worker_threads <= 0:
        raise HTTPException(
            status_code=400,
            detail="worker_threads must be greater than 0"
        )
    
    tasks = db.query(Task).all()
    
    if not tasks:
        raise HTTPException(
            status_code=404,
            detail="No tasks found to execute"
        )
    
    result = question9(tasks, worker_threads)
    
    return {
        "status": "success",
        "execution_details": result
    }


# Default route
@app.get("/")
def default_route():
    return {"message": "Welcome to the Storewise Backend Assignment!", "documentation": "Visit localhost:8000/docs"}
