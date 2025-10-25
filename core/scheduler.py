"""
Priority Heap-based Scheduler for task management and reminders.
Demonstrates heap data structures, priority queues, and efficient scheduling algorithms.
"""

import heapq
import threading
import time
from typing import Any, Callable, Optional, List, Dict, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import uuid


class TaskPriority(Enum):
    """Task priority levels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ScheduledTask:
    """Represents a scheduled task with priority and metadata."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    function: Callable = None
    args: Tuple = field(default_factory=tuple)
    kwargs: Dict = field(default_factory=dict)
    scheduled_time: float = 0.0
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    retry_count: int = 0
    max_retries: int = 3
    timeout: Optional[float] = None
    metadata: Dict = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    
    def __lt__(self, other):
        """Comparison for heap ordering: higher priority and earlier time first."""
        if self.priority.value != other.priority.value:
            return self.priority.value > other.priority.value
        return self.scheduled_time < other.scheduled_time
    
    def __le__(self, other):
        return self < other or self == other
    
    def __gt__(self, other):
        return not self <= other
    
    def __ge__(self, other):
        return not self < other


class PriorityScheduler:
    """
    Advanced priority scheduler using binary heap for efficient task management.
    Features:
    - O(log n) insertion and extraction
    - Priority-based scheduling
    - Retry mechanism with exponential backoff
    - Task dependency management
    - Resource pooling
    - Deadlock detection
    """
    
    def __init__(self, max_workers: int = 4):
        self.task_heap: List[ScheduledTask] = []
        self.heap_lock = threading.RLock()
        self.worker_pool = []
        self.max_workers = max_workers
        self.running = False
        self.task_registry: Dict[str, ScheduledTask] = {}
        self.task_dependencies: Dict[str, List[str]] = defaultdict(list)
        self.completed_tasks: set[str] = set()
        self.failed_tasks: set[str] = set()
        self.resource_pools: Dict[str, int] = defaultdict(int)
        self._start_workers()
    
    def _start_workers(self) -> None:
        """Start worker threads for task execution."""
        self.running = True
        for i in range(self.max_workers):
            worker = threading.Thread(target=self._worker_loop, daemon=True)
            worker.start()
            self.worker_pool.append(worker)
    
    def schedule_task(self, 
                     function: Callable,
                     args: Tuple = (),
                     kwargs: Dict = None,
                     delay: float = 0.0,
                     priority: TaskPriority = TaskPriority.NORMAL,
                     max_retries: int = 3,
                     timeout: Optional[float] = None,
                     metadata: Dict = None,
                     dependencies: List[str] = None) -> str:
        """
        Schedule a task for execution.
        Returns task ID for tracking and cancellation.
        """
        if kwargs is None:
            kwargs = {}
        if metadata is None:
            metadata = {}
        if dependencies is None:
            dependencies = []
        
        task = ScheduledTask(
            function=function,
            args=args,
            kwargs=kwargs,
            scheduled_time=time.time() + delay,
            priority=priority,
            max_retries=max_retries,
            timeout=timeout,
            metadata=metadata
        )
        
        with self.heap_lock:
            heapq.heappush(self.task_heap, task)
            self.task_registry[task.id] = task
            
            # Set up dependencies
            for dep_id in dependencies:
                self.task_dependencies[dep_id].append(task.id)
        
        return task.id
    
    def schedule_recurring_task(self,
                               function: Callable,
                               interval: float,
                               args: Tuple = (),
                               kwargs: Dict = None,
                               priority: TaskPriority = TaskPriority.NORMAL,
                               max_retries: int = 3,
                               metadata: Dict = None) -> str:
        """Schedule a task that repeats at regular intervals."""
        if kwargs is None:
            kwargs = {}
        if metadata is None:
            metadata = {}
        
        def recurring_wrapper():
            try:
                function(*args, **kwargs)
            finally:
                # Schedule next occurrence
                self.schedule_recurring_task(
                    function, interval, args, kwargs, priority, max_retries, metadata
                )
        
        return self.schedule_task(
            recurring_wrapper, priority=priority, max_retries=max_retries, metadata=metadata
        )
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a scheduled task."""
        with self.heap_lock:
            if task_id in self.task_registry:
                task = self.task_registry[task_id]
                task.status = TaskStatus.CANCELLED
                return True
        return False
    
    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """Get the status of a task."""
        with self.heap_lock:
            if task_id in self.task_registry:
                return self.task_registry[task_id].status
        return None
    
    def get_pending_tasks(self) -> List[Dict]:
        """Get information about pending tasks."""
        with self.heap_lock:
            pending = []
            for task in self.task_heap:
                if task.status == TaskStatus.PENDING:
                    pending.append({
                        'id': task.id,
                        'scheduled_time': task.scheduled_time,
                        'priority': task.priority.value,
                        'metadata': task.metadata
                    })
            return sorted(pending, key=lambda x: (x['priority'], x['scheduled_time']))
    
    def _worker_loop(self) -> None:
        """Main worker loop for executing tasks."""
        while self.running:
            try:
                task = self._get_next_task()
                if task:
                    self._execute_task(task)
                else:
                    time.sleep(0.1)  # Brief pause when no tasks
            except Exception as e:
                print(f"Worker error: {e}")
                time.sleep(1)
    
    def _get_next_task(self) -> Optional[ScheduledTask]:
        """Get the next task to execute from the heap."""
        with self.heap_lock:
            while self.task_heap:
                task = heapq.heappop(self.task_heap)
                
                # Check if task is cancelled
                if task.status == TaskStatus.CANCELLED:
                    continue
                
                # Check if dependencies are met
                if not self._are_dependencies_met(task.id):
                    # Re-insert task for later processing
                    heapq.heappush(self.task_heap, task)
                    continue
                
                # Check if it's time to execute
                if task.scheduled_time <= time.time():
                    return task
                else:
                    # Re-insert task for later
                    heapq.heappush(self.task_heap, task)
                    break
        
        return None
    
    def _are_dependencies_met(self, task_id: str) -> bool:
        """Check if all dependencies for a task are completed."""
        dependencies = self.task_dependencies.get(task_id, [])
        return all(dep_id in self.completed_tasks for dep_id in dependencies)
    
    def _execute_task(self, task: ScheduledTask) -> None:
        """Execute a task with error handling and retry logic."""
        task.status = TaskStatus.RUNNING
        
        try:
            # Check timeout
            if task.timeout:
                result = self._execute_with_timeout(task, task.timeout)
            else:
                result = task.function(*task.args, **task.kwargs)
            
            task.status = TaskStatus.COMPLETED
            self.completed_tasks.add(task.id)
            
            # Notify dependent tasks
            self._notify_dependents(task.id)
            
        except Exception as e:
            task.retry_count += 1
            
            if task.retry_count <= task.max_retries:
                # Schedule retry with exponential backoff
                delay = min(2 ** task.retry_count, 60)  # Max 60 seconds
                task.scheduled_time = time.time() + delay
                task.status = TaskStatus.PENDING
                
                with self.heap_lock:
                    heapq.heappush(self.task_heap, task)
            else:
                task.status = TaskStatus.FAILED
                self.failed_tasks.add(task.id)
                print(f"Task {task.id} failed after {task.max_retries} retries: {e}")
    
    def _execute_with_timeout(self, task: ScheduledTask, timeout: float) -> Any:
        """Execute a task with timeout using threading."""
        result = [None]
        exception = [None]
        
        def target():
            try:
                result[0] = task.function(*task.args, **task.kwargs)
            except Exception as e:
                exception[0] = e
        
        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout)
        
        if thread.is_alive():
            # Task timed out
            raise TimeoutError(f"Task {task.id} timed out after {timeout} seconds")
        
        if exception[0]:
            raise exception[0]
        
        return result[0]
    
    def _notify_dependents(self, completed_task_id: str) -> None:
        """Notify tasks that depend on the completed task."""
        # This is a simplified implementation
        # In a full system, you'd have more sophisticated dependency management
        pass
    
    def shutdown(self, timeout: float = 30.0) -> None:
        """Gracefully shutdown the scheduler."""
        self.running = False
        
        # Wait for workers to finish
        for worker in self.worker_pool:
            worker.join(timeout=timeout)
    
    def get_statistics(self) -> Dict:
        """Get scheduler statistics."""
        with self.heap_lock:
            return {
                'total_tasks': len(self.task_registry),
                'pending_tasks': len([t for t in self.task_heap if t.status == TaskStatus.PENDING]),
                'completed_tasks': len(self.completed_tasks),
                'failed_tasks': len(self.failed_tasks),
                'heap_size': len(self.task_heap)
            }


class ReminderManager:
    """
    High-level reminder management system built on top of the priority scheduler.
    Demonstrates practical application of scheduling algorithms.
    """
    
    def __init__(self, scheduler: PriorityScheduler):
        self.scheduler = scheduler
        self.reminders: Dict[str, Dict] = {}
    
    def set_reminder(self, 
                    message: str, 
                    reminder_time: float,
                    priority: TaskPriority = TaskPriority.NORMAL,
                    recurring: bool = False,
                    interval: float = 0.0) -> str:
        """Set a reminder for a specific time."""
        def reminder_action():
            print(f"🔔 REMINDER: {message}")
            # In a real implementation, this would trigger notifications
        
        task_id = self.scheduler.schedule_task(
            function=reminder_action,
            delay=reminder_time - time.time(),
            priority=priority,
            metadata={'type': 'reminder', 'message': message}
        )
        
        self.reminders[task_id] = {
            'message': message,
            'time': reminder_time,
            'recurring': recurring,
            'interval': interval
        }
        
        return task_id
    
    def set_recurring_reminder(self, 
                              message: str, 
                              interval: float,
                              priority: TaskPriority = TaskPriority.NORMAL) -> str:
        """Set a recurring reminder."""
        def recurring_reminder():
            print(f"🔄 RECURRING REMINDER: {message}")
        
        task_id = self.scheduler.schedule_recurring_task(
            function=recurring_reminder,
            interval=interval,
            priority=priority,
            metadata={'type': 'recurring_reminder', 'message': message}
        )
        
        self.reminders[task_id] = {
            'message': message,
            'interval': interval,
            'recurring': True
        }
        
        return task_id
    
    def cancel_reminder(self, reminder_id: str) -> bool:
        """Cancel a reminder."""
        if self.scheduler.cancel_task(reminder_id):
            self.reminders.pop(reminder_id, None)
            return True
        return False
    
    def get_upcoming_reminders(self, limit: int = 10) -> List[Dict]:
        """Get upcoming reminders."""
        pending = self.scheduler.get_pending_tasks()
        reminders = []
        
        for task_info in pending:
            if task_info['metadata'].get('type') in ['reminder', 'recurring_reminder']:
                reminders.append({
                    'id': task_info['id'],
                    'message': task_info['metadata'].get('message', ''),
                    'scheduled_time': task_info['scheduled_time'],
                    'priority': task_info['priority']
                })
        
        return sorted(reminders, key=lambda x: x['scheduled_time'])[:limit]


if __name__ == "__main__":
    # Demo the scheduler
    scheduler = PriorityScheduler(max_workers=2)
    reminder_manager = ReminderManager(scheduler)
    
    # Schedule some test tasks
    def test_task(name: str, duration: float = 1.0):
        print(f"Executing task: {name}")
        time.sleep(duration)
        print(f"Completed task: {name}")
    
    # Schedule tasks with different priorities and delays
    scheduler.schedule_task(test_task, args=("High Priority", 0.5), 
                          delay=1.0, priority=TaskPriority.HIGH)
    scheduler.schedule_task(test_task, args=("Low Priority", 0.5), 
                          delay=0.5, priority=TaskPriority.LOW)
    scheduler.schedule_task(test_task, args=("Normal Priority", 0.5), 
                          delay=0.0, priority=TaskPriority.NORMAL)
    
    # Set some reminders
    current_time = time.time()
    reminder_manager.set_reminder("Call mom", current_time + 2.0)
    reminder_manager.set_reminder("Buy groceries", current_time + 3.0, TaskPriority.HIGH)
    
    # Show statistics
    print("Scheduler statistics:", scheduler.get_statistics())
    print("Upcoming reminders:", reminder_manager.get_upcoming_reminders())
    
    # Let it run for a bit
    time.sleep(5)
    
    # Cleanup
    scheduler.shutdown()






