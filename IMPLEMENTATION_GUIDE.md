"""
QUESTIONS 7-9 IMPLEMENTATION GUIDE
====================================

PROJECT CONTEXT:
- Each task has: id, name, parent_id, created_at, due_date, priority, status, duration
- Tasks form a tree structure through parent_id relationships

===============================================
QUESTION 7: Task Relationship Determination
===============================================

PROBLEM:
Determine if one task is a direct or indirect subtask of another.
Example: If A → B → C (A is parent of B, B is parent of C)
Then C is a subtask of A

SOLUTION APPROACH:
1. Create a hash map for O(1) task lookup: task_id → Task
2. Implement is_subtask(child, parent) function:
   - Start from child task
   - Traverse up the parent chain using the map
   - If we reach the parent ID, return True
   - If parent_id is None (root reached), return False
3. Check both directions:
   - is_subtask(id1, id2) → id1 is subtask of id2
   - is_subtask(id2, id1) → id2 is subtask of id1
   - Otherwise → "NONE"

TIME COMPLEXITY: O(n + h*2)
- n = number of tasks (for building map)
- h = maximum depth of tree (for traversal)
- Usually h << n, so effectively O(n)

SPACE COMPLEXITY: O(n) for task map

CODE LOCATION: task_logic.py → question7() function

ENDPOINT: GET /tasks/question7?id1=<task_id>&id2=<task_id>

EXAMPLE:
If Tasks: 1(root), 2(parent=1), 3(parent=2), 4(parent=1)
- question7(tasks, 3, 1) → "Task 3 is a subtask of Task 1"
- question7(tasks, 2, 4) → "NONE"


===============================================
QUESTION 8: Date Range SQL Query
===============================================

PROBLEM:
Get tasks created between 26 Aug 2024 and 9 Sep 2024:
✓ Exclude completed tasks
✓ Exclude tasks created on Sunday
✓ Must work with SQLite and PostgreSQL

SOLUTION APPROACH:
1. Database Agnostic ORM Query (Recommended):
   - Use SQLAlchemy filters for database compatibility
   - Filter by created_at date range
   - Filter by status != 'completed'
   - Filter Sunday by weekday() != 6 in Python
   
2. Alternative Raw SQL Query:
   - For SQLite: Use strftime('%w', created_at) for weekday
   - For PostgreSQL: Use EXTRACT(DOW FROM created_at)
   - Wrap in different function based on DB type

WHY SUNDAY FILTERING IN PYTHON?
- SQLite uses different date functions than PostgreSQL
- Filtering in Python avoids database-specific SQL
- More maintainable and readable code

DATE LOGIC:
- Python weekday(): Monday=0, Sunday=6
- Include created_at >= 2024-08-26 AND <= 2024-09-09
- Exclude status = 'completed'
- Exclude weekday() == 6

ENDPOINTS:
- Primary: GET /tasks/question8/
  (Uses SQLAlchemy ORM - database agnostic)
- Alternative: GET /tasks/question8/raw-sql
  (Uses raw SQL for demonstration)

EXAMPLE RESPONSE:
{
  "status": "success",
  "count": 5,
  "date_range": {"start": "2024-08-26", "end": "2024-09-09"},
  "filters_applied": [
    "created_between_26aug_9sep_2024",
    "exclude_completed_tasks",
    "exclude_sunday_created"
  ],
  "tasks": [...]
}


===============================================
QUESTION 9: Asynchronous Task Execution
===============================================

PROBLEM:
Simulate asynchronous task execution with:
✓ Limited worker threads (thread pool)
✓ Task duration: execution_time = duration / 10 seconds
✓ Workers pick next task when free
✓ Proper async/threading patterns

SOLUTION APPROACH:
Architecture:
┌─────────────────────────────────────┐
│  ThreadPoolExecutor (max_workers=N) │
├─────────────────────────────────────┤
│  Worker 1  │  Worker 2  │ ... │  Worker N │
│  ↓         │  ↓         │     │  ↓       │
│ Task 1    │ Task 2    │ ... │ Task N   │
└─────────────────────────────────────┘

Implementation Details:
1. ThreadPoolExecutor with max_workers = worker_threads parameter
2. For each task:
   - Calculate execution_time = duration / 10.0
   - Sleep for execution_time seconds (simulates work)
   - Record start and end times
   - Store result in thread-safe execution log

3. Synchronization:
   - Use threading.Lock for execution_log updates
   - Ensures no race conditions when multiple workers log results
   - Each worker thread has exclusive access to shared resources

4. Scalability:
   - ThreadPoolExecutor manages thread creation/destruction
   - Automatic task queue management
   - Futures for tracking completion

TASK EXECUTION FLOW:
1. Create ThreadPoolExecutor with N workers
2. Submit M tasks to executor
3. Each worker picks up next available task
4. Worker executes task: sleep(duration/10)
5. Record execution details in thread-safe log
6. Wait for all tasks to complete
7. Return comprehensive execution report

TIME COMPLEXITY: O(total_duration / worker_threads)
- If 10 tasks of 5 seconds each = 50 seconds total
- With 5 workers: ~10 seconds execution time

SPACE COMPLEXITY: O(worker_threads + tasks)
- Worker threads in memory
- Execution log entries

CODE LOCATION: task_logic.py → question9() function

ENDPOINT: POST /tasks/question9/{worker_threads}

EXAMPLE RESPONSE:
{
  "status": "success",
  "execution_details": {
    "status": "completed",
    "summary": {
      "total_tasks": 10,
      "completed_tasks": 10,
      "failed_tasks": 0,
      "worker_threads": 4,
      "total_execution_time": 12.5
    },
    "execution_log": [
      {
        "task_id": 1,
        "task_name": "Task 1",
        "status": "completed",
        "scheduled_duration": 0.5,
        "actual_duration": 0.502,
        "priority": 1,
        "timestamp": "2024-04-05T10:30:45.123456"
      },
      ...
    ]
  }
}


===============================================
KEY DESIGN DECISIONS
===============================================

1. QUESTION 7 - O(n) Solution:
   ✓ Hash map for O(1) lookup instead of nested loops
   ✓ Linear traversal from child to parent
   ✓ Avoids O(n²) complexity of checking all pairs

2. QUESTION 8 - Database Agnostic:
   ✓ SQLAlchemy ORM for compatibility with multiple DB
   ✓ Sunday filtering in Python for easier maintenance
   ✓ Alternative raw SQL for advanced users

3. QUESTION 9 - Threading Best Practices:
   ✓ ThreadPoolExecutor for thread management
   ✓ Locks for thread-safe shared state
   ✓ Proper error handling with try-except
   ✓ Detailed execution logging for monitoring


===============================================
TESTING RECOMMENDATIONS
===============================================

Question 7:
- Test with:
  * Valid parent-child relationship
  * Multiple levels of hierarchy
  * Non-existent tasks
  * Tasks with no relationship

Question 8:
- Create test tasks with:
  * Various dates in range
  * Various dates outside range
  * Status values (pending, completed, in_progress)
  * Different weekdays

Question 9:
- Test with:
  * Different worker thread counts (1, 5, 10)
  * Different task counts
  * Various duration values
  * Edge cases (0 workers, 1 task, 100 tasks)


===============================================
PERFORMANCE NOTES
===============================================

Question 7:
- Best case: O(h) - shallow tree
- Worst case: O(n) - linear chain
- Real world: O(h) where h typically 3-5 levels

Question 8:
- ORM query: 1 DB query + Python filtering
- Raw SQL: 1 optimized DB query
- For large datasets, raw SQL may be faster

Question 9:
- Linear scaling with worker count
- 10 workers, 10 short tasks ≈ same time as 1 worker, 1 task
- Reduces total execution time by factor of min(worker_count, total_tasks)
"""
