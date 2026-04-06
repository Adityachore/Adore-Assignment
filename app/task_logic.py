from fastapi import HTTPException
from datetime import datetime, timedelta
from rapidfuzz import fuzz

def question2(tasks):
    groups={}

    for task in tasks:
        parent=task.parent_id

        if parent not in groups:
            groups[parent]=[]
        

        groups[parent].append(task)

    for parent in groups:
        groups[parent].sort(key=lambda x:x.created_at,reverse=True   )

    return groups



def question3(tasks):
    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)

    result = []

    for task in tasks:
        # Convert due_date to date (if it's datetime)
        due = task.due_date.date()

        if (due == today or due == tomorrow) and task.priority == 1:
            result.append(task)

    return result


def question4(tasks):
    
    parent_ids = set()

    for task in tasks:
        if task.parent_id is not None:
            parent_ids.add(task.parent_id)

    result = []

    for task in tasks:
        if task.id not in parent_ids:
            result.append(task)

    return result

def question5(tasks, task_id: int):
    target_task = None
    for task in tasks:
        if task.id == task_id:
            target_task = task
            break

    if not target_task:
        return 0

    parent = target_task.parent_id

    count = 0
    for task in tasks:
        if task.parent_id == parent and task.id != task_id:
            count += 1

    return count


def question6(tasks, query: str):
    result = []
    threshold=80

    for task in tasks:
        score=fuzz.ratio(query.lower(),task.name.lower())
        if score>=threshold:
            result.append(task)
    return result


def question7(tasks, id1, id2):
    """
    Determine the relationship between two tasks.
    
    Logic:
    - Create a hash map (task_id -> task) for O(1) lookup
    - For each task pair, traverse up the parent chain using the map
    - If one task is found as an ancestor of the other, return the relationship
    - If no relationship exists, return "NONE"
    
    Time Complexity: O(n + h*2) where n is number of tasks and h is max depth
    Space Complexity: O(n) for task map
    
    Args:
        tasks: List of Task objects
        id1: ID of first task
        id2: ID of second task
    
    Returns:
        String: Relationship between tasks or "NONE"
    """
    # Create a hash map for O(1) task lookup
    task_map = {task.id: task for task in tasks}
    
    def is_subtask(child, parent):
        """
        Check if child task is a direct or indirect subtask of parent task.
        Traverse up the parent chain from child to see if we reach parent.
        """
        curr = task_map.get(child)
        
        # Traverse up the parent chain
        while curr and curr.parent_id is not None:
            if curr.parent_id == parent:
                return True
            # Move to parent task
            curr = task_map.get(curr.parent_id)
        
        return False
    
    # Check both directions
    if is_subtask(id1, id2):
        return f"Task {id1} is a subtask of Task {id2}"
    elif is_subtask(id2, id1):
        return f"Task {id2} is a subtask of Task {id1}"
    else:
        return "NONE"


def question8_old(tasks, criteria: dict, sort_by: str):
    """
    This function is deprecated. Question 8 should be solved using raw SQL queries.
    Implementation is in main.py using SQLAlchemy raw SQL or ORM queries.
    """
    raise HTTPException(status_code=401, detail="For Question 8, use the SQL query endpoint in main.py")


import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict
import time as time_module


def question9(tasks: List, worker_threads: int):
    """
    Simulate asynchronous task execution with worker threads.
    
    Logic:
    - Use ThreadPoolExecutor to manage limited worker threads
    - Each task duration = duration / 10 seconds
    - Workers pick up tasks sequentially
    - Use asyncio to coordinate the execution
    - Return execution log with task execution details
    
    Time Complexity: O(total_duration / worker_threads)
    Space Complexity: O(worker_threads + tasks)
    
    Args:
        tasks: List of Task objects to execute
        worker_threads: Maximum number of concurrent worker threads
    
    Returns:
        Dict containing execution status and logs
    """
    
    if not tasks:
        return {"status": "no_tasks", "executed": []}
    
    if worker_threads <= 0:
        return {"status": "invalid_workers", "executed": []}
    
    # Store execution results
    execution_log = []
    execution_lock = threading.Lock()
    
    def execute_task(task):
        """
        Execute a single task in a worker thread.
        Simulates task execution by sleeping for duration/10 seconds.
        """
        try:
            # Calculate execution time: duration / 10 seconds
            execution_time = max(task.duration / 10.0, 0.1)  # Minimum 0.1 seconds
            
            # Record start time
            start_time = time_module.time()
            
            # Simulate task execution
            time_module.sleep(execution_time)
            
            # Record end time
            end_time = time_module.time()
            actual_duration = end_time - start_time
            
            # Add to execution log (thread-safe)
            with execution_lock:
                execution_log.append({
                    "task_id": task.id,
                    "task_name": task.name,
                    "status": "completed",
                    "scheduled_duration": execution_time,
                    "actual_duration": actual_duration,
                    "priority": task.priority,
                    "timestamp": datetime.now().isoformat()
                })
            
            return {
                "task_id": task.id,
                "status": "completed"
            }
        
        except Exception as e:
            # Handle execution errors
            with execution_lock:
                execution_log.append({
                    "task_id": task.id,
                    "task_name": task.name,
                    "status": "failed",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
            return {"task_id": task.id, "status": "failed"}
    
    # Execute tasks using ThreadPoolExecutor
    execution_results = []
    start_time = time_module.time()
    
    with ThreadPoolExecutor(max_workers=worker_threads) as executor:
        # Submit all tasks to the executor
        futures = [executor.submit(execute_task, task) for task in tasks]
        
        # Wait for all tasks to complete
        for future in futures:
            try:
                result = future.result()
                execution_results.append(result)
            except Exception as e:
                execution_results.append({"status": "error", "error": str(e)})
    
    total_time = time_module.time() - start_time
    
    # Return comprehensive execution report
    return {
        "status": "completed",
        "summary": {
            "total_tasks": len(tasks),
            "completed_tasks": len([r for r in execution_results if r.get("status") == "completed"]),
            "failed_tasks": len([r for r in execution_results if r.get("status") == "failed"]),
            "worker_threads": worker_threads,
            "total_execution_time": total_time
        },
        "execution_log": execution_log
    }