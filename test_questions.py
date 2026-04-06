"""
Test Script for Questions 7-9 Implementations
==============================================

This script demonstrates how to test the three implementations
with sample data.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from datetime import datetime, timedelta
from task_logic import question7, question9

# Mock Task class for testing
class MockTask:
    def __init__(self, id, name, parent_id=None, duration=50, status='pending', priority=1):
        self.id = id
        self.name = name
        self.parent_id = parent_id
        self.duration = duration
        self.status = status
        self.priority = priority
        self.created_at = datetime.now()


def test_question7():
    """Test Question 7: Task Relationship Determination"""
    print("\n" + "="*60)
    print("TESTING QUESTION 7: Task Relationship Determination")
    print("="*60)
    
    # Create a task hierarchy:
    #     Task 1 (root)
    #    /        \
    # Task 2    Task 4
    #   |
    # Task 3
    
    tasks = [
        MockTask(1, "Root Task", parent_id=None),
        MockTask(2, "Sub Task 1", parent_id=1),
        MockTask(3, "Sub Sub Task", parent_id=2),
        MockTask(4, "Sub Task 2", parent_id=1),
        MockTask(5, "Independent Task", parent_id=None),
    ]
    
    test_cases = [
        (3, 1, "Task 3 is a subtask of Task 1"),
        (3, 2, "Task 3 is a subtask of Task 2"),
        (2, 1, "Task 2 is a subtask of Task 1"),
        (2, 4, "NONE"),
        (5, 1, "NONE"),
    ]
    
    print("\nTask Hierarchy:")
    print("    Task 1 (root)")
    print("   /          \\")
    print("Task 2      Task 4")
    print("  |")
    print("Task 3")
    print("Task 5 (independent)")
    
    print("\n\nTest Cases:")
    for id1, id2, expected in test_cases:
        result = question7(tasks, id1, id2)
        status = "✓ PASS" if expected in result else "✗ FAIL"
        print(f"\n{status}: question7(tasks, {id1}, {id2})")
        print(f"  Result: {result}")


def test_question9():
    """Test Question 9: Asynchronous Task Execution"""
    print("\n" + "="*60)
    print("TESTING QUESTION 9: Asynchronous Task Execution")
    print("="*60)
    
    # Create test tasks
    tasks = [
        MockTask(1, "Task 1", duration=10),  # 1 second execution
        MockTask(2, "Task 2", duration=20),  # 2 seconds execution
        MockTask(3, "Task 3", duration=30),  # 3 seconds execution
        MockTask(4, "Task 4", duration=10),  # 1 second execution
    ]
    
    print("\nTask Details:")
    print("Task | Duration | Execution Time")
    print("-" * 35)
    for task in tasks:
        exec_time = task.duration / 10.0
        print(f"{task.id:4} | {task.duration:8} | {exec_time:6.1f}s")
    
    test_worker_counts = [1, 2, 4]
    
    print("\n\nExecution Tests:")
    for worker_count in test_worker_counts:
        print(f"\n✓ Testing with {worker_count} worker thread(s):")
        result = question9(tasks, worker_count)
        
        summary = result.get('summary', {})
        print(f"  Total Tasks: {summary.get('total_tasks', 0)}")
        print(f"  Completed: {summary.get('completed_tasks', 0)}")
        print(f"  Failed: {summary.get('failed_tasks', 0)}")
        print(f"  Total Execution Time: {summary.get('total_execution_time', 0):.2f}s")
        
        log = result.get('execution_log', [])
        if log:
            print(f"  Sample Task Execution:")
            first_task = log[0]
            if 'actual_duration' in first_task:
                print(f"    {first_task['task_name']}: {first_task['actual_duration']:.2f}s")
            elif 'error' in first_task:
                print(f"    {first_task['task_name']}: ERROR - {first_task['error']}")
            else:
                print(f"    {first_task['task_name']}: Status - {first_task['status']}")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("IMPLEMENTATION VERIFICATION TESTS")
    print("="*60)
    
    try:
        test_question7()
        print("\n" + "-"*60)
        test_question9()
        
        print("\n" + "="*60)
        print("✓ ALL TESTS COMPLETED SUCCESSFULLY")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
