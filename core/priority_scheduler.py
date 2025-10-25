"""
Priority Scheduler - Manages skill execution priority and scheduling
"""

from typing import List, Optional, Callable, Any
from enum import Enum
import heapq
import time
from dataclasses import dataclass, field
from skills.base_skill import BaseSkill, SkillPriority


@dataclass
class ScheduledTask:
    """Represents a scheduled task"""
    skill: BaseSkill
    priority: int
    scheduled_time: float
    context: Any = None
    callback: Optional[Callable] = None
    task_id: str = field(default_factory=lambda: str(time.time()))
    
    def __lt__(self, other):
        """For heapq comparison - higher priority first, then earlier time"""
        if self.priority != other.priority:
            return self.priority > other.priority
        return self.scheduled_time < other.scheduled_time


class PriorityScheduler:
    """Schedules and manages skill execution based on priority"""
    
    def __init__(self):
        self.task_queue: List[ScheduledTask] = []
        self.completed_tasks: List[ScheduledTask] = []
        self.running_tasks: List[ScheduledTask] = []
        self.task_counter = 0
    
    def schedule_skill(self, skill: BaseSkill, context: Any = None, 
                      delay: float = 0.0, callback: Optional[Callable] = None) -> str:
        """Schedule a skill for execution"""
        scheduled_time = time.time() + delay
        priority = self._get_priority_value(skill.priority)
        
        task = ScheduledTask(
            skill=skill,
            priority=priority,
            scheduled_time=scheduled_time,
            context=context,
            callback=callback,
            task_id=f"task_{self.task_counter}_{int(time.time())}"
        )
        
        heapq.heappush(self.task_queue, task)
        self.task_counter += 1
        
        return task.task_id
    
    def schedule_immediate(self, skill: BaseSkill, context: Any = None, 
                          callback: Optional[Callable] = None) -> str:
        """Schedule a skill for immediate execution"""
        return self.schedule_skill(skill, context, delay=0.0, callback=callback)
    
    def schedule_delayed(self, skill: BaseSkill, delay: float, context: Any = None,
                        callback: Optional[Callable] = None) -> str:
        """Schedule a skill for delayed execution"""
        return self.schedule_skill(skill, context, delay=delay, callback=callback)
    
    def get_next_task(self) -> Optional[ScheduledTask]:
        """Get the next task to execute"""
        if not self.task_queue:
            return None
        
        current_time = time.time()
        
        # Check if the highest priority task is ready
        if self.task_queue[0].scheduled_time <= current_time:
            return heapq.heappop(self.task_queue)
        
        return None
    
    def execute_next(self) -> bool:
        """Execute the next ready task"""
        task = self.get_next_task()
        if not task:
            return False
        
        try:
            # Move to running tasks
            self.running_tasks.append(task)
            
            # Execute the skill
            if task.context:
                result = task.skill.execute(task.context)
            else:
                # Create a minimal context if none provided
                from skills.base_skill import SkillContext
                context = SkillContext(
                    user_input="scheduled_task",
                    confidence=1.0,
                    metadata={"scheduled": True, "task_id": task.task_id}
                )
                result = task.skill.execute(context)
            
            # Execute callback if provided
            if task.callback:
                task.callback(result, task)
            
            # Move to completed tasks
            self.running_tasks.remove(task)
            self.completed_tasks.append(task)
            
            return True
            
        except Exception as e:
            # Handle execution error
            print(f"Error executing scheduled task {task.task_id}: {e}")
            self.running_tasks.remove(task)
            self.completed_tasks.append(task)
            return False
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a scheduled task"""
        # Check in task queue
        for i, task in enumerate(self.task_queue):
            if task.task_id == task_id:
                self.task_queue.pop(i)
                heapq.heapify(self.task_queue)  # Re-heapify after removal
                return True
        
        # Check in running tasks
        for task in self.running_tasks:
            if task.task_id == task_id:
                self.running_tasks.remove(task)
                return True
        
        return False
    
    def get_queue_status(self) -> dict:
        """Get current queue status"""
        current_time = time.time()
        
        return {
            "total_queued": len(self.task_queue),
            "total_running": len(self.running_tasks),
            "total_completed": len(self.completed_tasks),
            "next_task_time": self.task_queue[0].scheduled_time if self.task_queue else None,
            "next_task_delay": max(0, self.task_queue[0].scheduled_time - current_time) if self.task_queue else None,
            "ready_tasks": len([t for t in self.task_queue if t.scheduled_time <= current_time])
        }
    
    def clear_completed(self) -> int:
        """Clear completed tasks and return count"""
        count = len(self.completed_tasks)
        self.completed_tasks.clear()
        return count
    
    def clear_all(self) -> None:
        """Clear all tasks"""
        self.task_queue.clear()
        self.completed_tasks.clear()
        self.running_tasks.clear()
        self.task_counter = 0
    
    def get_task_by_id(self, task_id: str) -> Optional[ScheduledTask]:
        """Get a task by its ID"""
        # Check all task lists
        for task in self.task_queue + self.running_tasks + self.completed_tasks:
            if task.task_id == task_id:
                return task
        return None
    
    def reschedule_task(self, task_id: str, new_delay: float) -> bool:
        """Reschedule a task with a new delay"""
        task = self.get_task_by_id(task_id)
        if not task:
            return False
        
        # Cancel the existing task
        self.cancel_task(task_id)
        
        # Schedule with new delay
        new_task_id = self.schedule_skill(
            task.skill, 
            task.context, 
            delay=new_delay, 
            callback=task.callback
        )
        
        return new_task_id is not None
    
    def _get_priority_value(self, priority: SkillPriority) -> int:
        """Convert SkillPriority enum to integer value for comparison"""
        priority_values = {
            SkillPriority.LOW: 1,
            SkillPriority.NORMAL: 2,
            SkillPriority.HIGH: 3,
            SkillPriority.CRITICAL: 4
        }
        return priority_values.get(priority, 2)
    
    def get_priority_stats(self) -> dict:
        """Get statistics about task priorities"""
        priority_counts = {}
        
        for task in self.task_queue + self.running_tasks + self.completed_tasks:
            priority_name = task.skill.priority.name
            priority_counts[priority_name] = priority_counts.get(priority_name, 0) + 1
        
        return priority_counts
    
    def run_until_empty(self, max_executions: int = 100) -> int:
        """Run scheduler until queue is empty or max executions reached"""
        executions = 0
        while self.task_queue and executions < max_executions:
            if self.execute_next():
                executions += 1
            else:
                break
        return executions
