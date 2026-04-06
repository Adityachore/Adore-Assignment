
# Storewise Task Manager Backend - Assignment Complete ✅

**Status:** All 9 Questions Implemented & Tested  
**Last Updated:** April 6, 2026  
**Assignment Level:** Level 1 + Level 2 (Complete)

---

## 📋 Assignment Overview

This project implements a **task management system backend** using FastAPI and SQLAlchemy. The assignment consists of 9 progressive tasks that test Python proficiency, database operations, algorithm design, and concurrent programming.

### What Was Accomplished

✅ **Level 1 (Questions 1-6):** Basic CRUD operations and data manipulation  
✅ **Level 2 (Questions 7-9):** Advanced algorithms, SQL queries, and async programming  
✅ **All endpoints working** with proper error handling  
✅ **Complete test suite** for validation  
✅ **Production-ready code** with optimization

---

## 🎯 Questions Completed

### Level 1 - Foundational Tasks ✅

| Q | Task | Implementation | Complexity |
|---|------|---|---|
| **1** | CRUD: Get/Create/Delete Tasks | `app/main.py` endpoints | Easy |
| **2** | Group tasks by parent_id, sort by creation date | `task_logic.py` - `question2()` | Easy |
| **3** | Filter: Today/Tomorrow due date + Priority=1 | `task_logic.py` - `question3()` | Easy |
| **4** | Find parent tasks with no children | `task_logic.py` - `question4()` | Easy |
| **5** | Count sibling tasks | `task_logic.py` - `question5(task_id)` | Easy |
| **6** | Fuzzy search by task name | `task_logic.py` - `question6(query)` | Moderate |

### Level 2 - Advanced Tasks ✅

| Q | Task | Implementation | Complexity | Key Achievement |
|---|------|---|---|---|
| **7** | Task relationship determination | `task_logic.py` - `question7(id1, id2)` | Hard | **O(n) solution** with bug fix |
| **8** | SQL date range query with filters | `app/main.py` - `question8_route()` | Hard | **Database agnostic** design |
| **9** | Async task execution with workers | `task_logic.py` - `question9(tasks, workers)` | Hard | **Thread-safe** implementation |

---

## 🛠 Prerequisites & Setup

**Requirements:**
- Python 3.8+
- pip package manager
- FastAPI framework
- SQLAlchemy ORM

**Installation:**
```bash
# Clone the repository
git clone https://github.com/Adityachore/Adore-Assignment.git
cd storewise-backend-assignment

# Install dependencies
pip install -r requirements.txt

# Navigate to app directory
cd app

# Start FastAPI server
fastapi dev
# or
python main.py
```

**Access API Documentation:**
```
http://localhost:8000/docs
```

---

## 📊 Implementation Details

### Question 1-6: Level 1 Tasks
**What was learned:**
- FastAPI routing and dependency injection
- Pydantic models for request validation
- SQLAlchemy ORM queries
- Data manipulation and filtering
- String matching with fuzzy search (RapidFuzz library)

### Question 7: Task Relationship Determination ⭐

**Challenge:** Determine if one task is a subtask of another (direct or indirect)

**Solution Implemented:**
```python
def question7(tasks, id1, id2):
    # Create hash map for O(1) lookup
    task_map = {task.id: task for task in tasks}
    
    def is_subtask(child, parent):
        curr = task_map.get(child)
        while curr and curr.parent_id is not None:
            if curr.parent_id == parent:
                return True
            curr = task_map.get(curr.parent_id)
        return False
    
    # Check both directions
    if is_subtask(id1, id2):
        return f"Task {id1} is a subtask of Task {id2}"
    elif is_subtask(id2, id1):
        return f"Task {id2} is a subtask of Task {id1}"
    else:
        return "NONE"
```

**Key Learning:**
- **Algorithm Optimization:** Changed from nested loops O(n²) to hash map O(n)
- **Graph Traversal:** Parent chain traversal using hash lookups
- **Bug Fix:** Fixed variable naming error in original code (`current` → `curr`)

**Performance:**
- Time Complexity: O(n + h) where h = tree depth
- Space Complexity: O(n) for task map

### Question 8: SQL Date Range Query ⭐

**Challenge:** Query tasks with multiple filters (date range + status + day of week)

**Filters Applied:**
1. Created between Aug 26 - Sep 9, 2024
2. Exclude completed status
3. Exclude Sunday (day 6 in weekday())

**Solution Implemented:**
```python
@app.get("/tasks/question8/")
def question8_route(db: Session = Depends(get_db)):
    # SQLAlchemy ORM for database compatibility
    tasks = db.query(Task).filter(
        and_(
            Task.created_at >= datetime(2024, 8, 26),
            Task.created_at <= datetime(2024, 9, 9),
            Task.status != 'completed'
        )
    ).all()
    
    # Python-based weekday filtering
    filtered_tasks = [
        task for task in tasks 
        if task.created_at.weekday() != 6  # 6 = Sunday
    ]
    
    return {
        "status": "success",
        "count": len(filtered_tasks),
        "date_range": {...},
        "filters_applied": [...],
        "tasks": filtered_tasks
    }
```

**Key Learning:**
- **Database Agnostic Design:** Avoid DB-specific functions (strftime, EXTRACT)
- **Hybrid Approach:** Use ORM + Python filtering for compatibility
- **SQLite vs PostgreSQL:** Both supported without code changes

### Question 9: Asynchronous Task Execution ⭐

**Challenge:** Execute tasks with limited worker threads, measuring performance gains

**Solution Implemented:**
```python
def question9(tasks, worker_threads):
    execution_log = []
    execution_lock = threading.Lock()
    
    def execute_task(task):
        execution_time = task.duration / 10.0
        start_time = time.time()
        time.sleep(execution_time)  # Simulate work
        elapsed = time.time() - start_time
        
        with execution_lock:
            execution_log.append({
                'task_id': task.id,
                'status': 'completed',
                'actual_duration': elapsed
            })
    
    # Use ThreadPoolExecutor for worker management
    with ThreadPoolExecutor(max_workers=worker_threads) as executor:
        futures = [executor.submit(execute_task, task) for task in tasks]
        for future in futures:
            future.result()
    
    return {
        "status": "completed",
        "summary": {...},
        "execution_log": execution_log
    }
```

**Performance Analysis:**
```
4 tasks (1s + 2s + 3s + 1s = 7s total):

Workers: 1  → ~7.00s (sequential)
Workers: 2  → ~4.00s (parallel pairs)
Workers: 4  → ~3.00s (all parallel)
Workers: 8  → ~3.00s (no improvement)

Scaling Factor: ~duration / worker_count (up to task limit)
```

**Key Learning:**
- **Thread Safety:** Use locks for concurrent access to shared resources
- **ThreadPoolExecutor:** Simplified thread management
- **Performance Scaling:** Linear improvement up to task count
- **Concurrent Programming:** Proper synchronization prevents race conditions

---

## 📚 What I Learned

### 1. Algorithm Optimization
- Identifying inefficient nested loops (O(n²))
- Hash maps for constant-time lookups O(1)
- Tree/graph traversal techniques

### 2. Database Design
- SQLAlchemy ORM vs Raw SQL tradeoffs
- Database-agnostic query design
- Compatibility across different database systems (SQLite, PostgreSQL)

### 3. Concurrent Programming
- ThreadPoolExecutor for managing worker threads
- Thread safety with locks (threading.Lock)
- Race condition prevention
- Performance measurements in concurrent systems

### 4. API Design
- FastAPI routing and dependency injection
- Request/Response validation with Pydantic
- Error handling and HTTP status codes
- API documentation with Swagger/OpenAPI

### 5. Code Quality
- Clean code principles
- Docstrings and comments
- Time/Space complexity analysis
- Testing and validation

### 6. Python Best Practices
- Efficient data structures (dict, set)
- Context managers (with statements)
- List comprehensions
- Exception handling

---

## 🧪 Testing

**Run Complete Test Suite:**
```bash
python test_questions.py
```

**Test Coverage:**
- Question 7: 5 test cases (relationship detection)
- Question 9: 3 configurations (1, 2, 4 workers)
- All edge cases and error scenarios

**Results:**
```
✅ Question 7: All relationship detection tests PASS
✅ Question 9: All worker thread configurations PASS
✅ Performance metrics validated
✅ Thread safety verified
```

---

## 📁 Project Structure

```
storewise-backend-assignment/
├── app/
│   ├── main.py                    # FastAPI endpoints (Q1-9)
│   ├── task_logic.py              # Business logic (Q1-9)
│   ├── models.py                  # SQLAlchemy models
│   └── tasks.db                   # SQLite database
│
├── test_questions.py              # Complete test suite
├── requirements.txt               # Python dependencies
├── QUESTIONS_7_9_README.md        # Q7-9 quick reference
├── IMPLEMENTATION_GUIDE.md        # Detailed algorithm explanations
├── API_REFERENCE.md               # API usage with examples
├── IMPLEMENTATION_SUMMARY.md      # Executive summary
├── CHECKLIST.md                   # Implementation checklist
└── README.md                      # This file
```

---

## 🚀 Key Achievements

✅ **All 9 Questions Completed:** Level 1 + Level 2 fully implemented  
✅ **Efficient Algorithms:** O(n) solutions where applicable  
✅ **Production-Ready Code:** Error handling, validation, documentation  
✅ **Test Coverage:** Comprehensive test suite with passing tests  
✅ **Database Compatibility:** Works with SQLite and PostgreSQL  
✅ **Thread Safety:** Proper synchronization in concurrent code  
✅ **Documentation:** 5 detailed guide files with examples  

---

## 📝 API Endpoints Summary

| Method | Endpoint | Question | Status |
|--------|----------|----------|--------|
| GET | `/tasks` | 1 | ✅ |
| POST | `/tasks` | 1 | ✅ |
| DELETE | `/tasks/{id}` | 1 | ✅ |
| GET | `/tasks/question2` | 2 | ✅ |
| GET | `/tasks/question3` | 3 | ✅ |
| GET | `/tasks/question4` | 4 | ✅ |
| GET | `/tasks/question5/{task_id}` | 5 | ✅ |
| GET | `/tasks/question6/{query}` | 6 | ✅ |
| GET | `/tasks/question7?id1=X&id2=Y` | 7 | ✅ |
| GET | `/tasks/question8/` | 8 | ✅ |
| POST | `/tasks/question9/{worker_threads}` | 9 | ✅ |

---

## 💡 Technical Highlights

- **Efficient Data Structures:** Hash maps, sets, lists
- **Algorithm Complexity Analysis:** O(n), O(n log n) where applicable
- **Concurrent Programming:** ThreadPoolExecutor with proper synchronization
- **Database Optimization:** ORM patterns with raw SQL fallback
- **Error Handling:** Comprehensive exception handling throughout
- **Code Documentation:** Docstrings and inline comments

---

## 🎓 Development Lessons

1. **Think Before Coding:** Algorithm design beats coding speed
2. **Trade-offs:** Understand ORM vs Raw SQL, simplicity vs performance
3. **Testing:** Write tests early to catch bugs and validate edge cases
4. **Documentation:** Clear documentation saves time for reviewers
5. **Code Review:** Lock usage and thread safety require careful review

---

## 📞 Questions or Issues?

Refer to:
- `IMPLEMENTATION_GUIDE.md` - Detailed algorithm explanations
- `API_REFERENCE.md` - API usage with curl/Python examples
- `test_questions.py` - Test examples and usage patterns
- Comments in `app/main.py` and `app/task_logic.py`

---

## ✨ Conclusion

This assignment successfully demonstrated:
- Full-stack backend development with FastAPI
- Algorithm optimization and complexity analysis
- Database design and SQL query optimization
- Concurrent programming with thread safety
- Professional code quality and documentation

**All objectives achieved. Assignment Complete!** 🎉

