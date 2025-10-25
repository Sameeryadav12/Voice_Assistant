"""
Smart To-Do & Notes Skill - Advanced task and note management
Provides comprehensive task tracking and quick note-taking capabilities.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from skills.base_skill import BaseSkill, SkillContext, SkillResult, SkillPriority
from dataclasses import dataclass, asdict
import re


@dataclass
class Note:
    """Represents a quick note."""
    id: int
    content: str
    created_at: str
    category: str = "general"
    
    def to_dict(self):
        return asdict(self)


@dataclass
class Task:
    """Represents a to-do task."""
    id: int
    title: str
    description: str
    priority: str  # high, medium, low
    status: str  # pending, in_progress, completed
    created_at: str
    due_date: Optional[str] = None
    completed_at: Optional[str] = None
    category: str = "general"
    
    def to_dict(self):
        return asdict(self)


class TodoNotesSkill(BaseSkill):
    """
    Advanced skill for managing tasks and notes.
    Features:
    - Quick voice notes
    - Task management with priorities
    - Due dates and reminders
    - Persistent storage
    - Export capabilities
    - Smart categorization
    """
    
    def __init__(self):
        super().__init__(
            name="todo_notes",
            description="Manage tasks and take notes",
            priority=SkillPriority.CRITICAL
        )
        
        # Storage paths
        self.data_dir = "data"
        self.notes_file = os.path.join(self.data_dir, "notes.json")
        self.tasks_file = os.path.join(self.data_dir, "tasks.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Load existing data
        self.notes = self._load_notes()
        self.tasks = self._load_tasks()
        
    def can_handle(self, context: SkillContext) -> bool:
        """Check if this skill can handle the request."""
        user_input = context.user_input.lower()
        
        # More flexible note keywords
        note_keywords = [
            "note", "write down", "remember this", "make a note",
            "save this", "jot down", "take a note", "note this",
            "write this down", "remember", "save", "record",
            "quick note", "memo", "write", "document", "capture"
        ]
        
        # More flexible task/todo keywords
        task_keywords = [
            "task", "todo", "to do", "to-do", "add task",
            "create task", "new task", "my tasks", "show tasks",
            "list tasks", "mark", "complete", "done", "finish",
            "delete task", "remove task", "checklist", "agenda",
            "schedule", "plan", "assignment", "job", "work",
            "show my tasks", "what tasks", "task list", "todo list"
        ]
        
        has_note = any(keyword in user_input for keyword in note_keywords)
        has_task = any(keyword in user_input for keyword in task_keywords)
        
        return has_note or has_task
    
    def execute(self, context: SkillContext) -> SkillResult:
        """Execute task or note command."""
        user_input = context.user_input.lower()
        
        try:
            # Determine command type
            if any(word in user_input for word in ["take a note", "make a note", "write down", "jot down", "save this", "remember this"]):
                return self._handle_add_note(user_input)
            
            elif any(word in user_input for word in ["show notes", "my notes", "list notes", "read notes", "what are my notes"]):
                return self._handle_list_notes()
            
            elif any(word in user_input for word in ["add task", "create task", "new task", "task:"]):
                return self._handle_add_task(user_input)
            
            elif any(word in user_input for word in ["show tasks", "my tasks", "list tasks", "what tasks", "to do list", "todo list"]):
                return self._handle_list_tasks(user_input)
            
            elif any(word in user_input for word in ["mark", "complete", "finish", "done"]) and ("task" in user_input or any(char.isdigit() for char in user_input)):
                return self._handle_complete_task(user_input)
            
            elif any(word in user_input for word in ["delete task", "remove task"]):
                return self._handle_delete_task(user_input)
            
            elif "export" in user_input:
                return self._handle_export()
            
            else:
                return SkillResult(
                    success=False,
                    message="I can help with notes and tasks. Try 'take a note' or 'add task'",
                    data={},
                    execution_time=0.0,
                    skill_name=self.name
                )
        
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Sorry, I encountered an error: {str(e)}",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error=str(e)
            )
    
    def _handle_add_note(self, user_input: str) -> SkillResult:
        """Add a new note."""
        start_time = datetime.now()
        
        # Extract note content
        content = self._extract_note_content(user_input)
        
        if not content:
            return SkillResult(
                success=False,
                message="I couldn't understand what you want me to note. Try: 'take a note: buy groceries'",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
        
        # Create note
        note_id = max([n.id for n in self.notes], default=0) + 1
        category = self._categorize_content(content)
        
        note = Note(
            id=note_id,
            content=content,
            created_at=datetime.now().isoformat(),
            category=category
        )
        
        self.notes.append(note)
        self._save_notes()
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        message = f"✅ Note saved: '{content}'\nCategory: {category}"
        
        return SkillResult(
            success=True,
            message=message,
            data={"note": note.to_dict()},
            execution_time=execution_time,
            skill_name=self.name
        )
    
    def _handle_list_notes(self) -> SkillResult:
        """List all notes."""
        start_time = datetime.now()
        
        if not self.notes:
            return SkillResult(
                success=True,
                message="📝 You have no notes yet. Say 'take a note' to create one!",
                data={"notes": []},
                execution_time=0.0,
                skill_name=self.name
            )
        
        # Sort notes by creation time (newest first)
        sorted_notes = sorted(self.notes, key=lambda n: n.created_at, reverse=True)
        
        message = f"📝 Your Notes ({len(sorted_notes)} total):\n\n"
        
        for note in sorted_notes[:10]:  # Show last 10 notes
            created = datetime.fromisoformat(note.created_at)
            time_str = created.strftime("%b %d, %I:%M %p")
            message += f"[{note.id}] {note.content}\n"
            message += f"    📅 {time_str} | 🏷️ {note.category}\n\n"
        
        if len(sorted_notes) > 10:
            message += f"... and {len(sorted_notes) - 10} more notes"
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return SkillResult(
            success=True,
            message=message.strip(),
            data={"notes": [n.to_dict() for n in sorted_notes]},
            execution_time=execution_time,
            skill_name=self.name
        )
    
    def _handle_add_task(self, user_input: str) -> SkillResult:
        """Add a new task."""
        start_time = datetime.now()
        
        # Extract task details
        task_title = self._extract_task_title(user_input)
        
        if not task_title:
            return SkillResult(
                success=False,
                message="I couldn't understand the task. Try: 'add task: finish project report'",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
        
        # Extract priority
        priority = self._extract_priority(user_input)
        
        # Extract due date
        due_date = self._extract_due_date(user_input)
        
        # Create task
        task_id = max([t.id for t in self.tasks], default=0) + 1
        category = self._categorize_content(task_title)
        
        task = Task(
            id=task_id,
            title=task_title,
            description="",
            priority=priority,
            status="pending",
            created_at=datetime.now().isoformat(),
            due_date=due_date,
            category=category
        )
        
        self.tasks.append(task)
        self._save_tasks()
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        message = f"✅ Task added: '{task_title}'\n"
        message += f"Priority: {priority.upper()}"
        if due_date:
            message += f"\nDue: {due_date}"
        message += f"\nCategory: {category}"
        
        return SkillResult(
            success=True,
            message=message,
            data={"task": task.to_dict()},
            execution_time=execution_time,
            skill_name=self.name
        )
    
    def _handle_list_tasks(self, user_input: str) -> SkillResult:
        """List tasks."""
        start_time = datetime.now()
        
        # Filter tasks based on status
        if "completed" in user_input or "done" in user_input:
            tasks = [t for t in self.tasks if t.status == "completed"]
            status_filter = "completed"
        else:
            tasks = [t for t in self.tasks if t.status != "completed"]
            status_filter = "active"
        
        if not tasks:
            message = f"📋 You have no {status_filter} tasks!"
            if status_filter == "active":
                message += " You're all caught up! 🎉"
            
            return SkillResult(
                success=True,
                message=message,
                data={"tasks": []},
                execution_time=0.0,
                skill_name=self.name
            )
        
        # Sort by priority and due date
        priority_order = {"high": 0, "medium": 1, "low": 2}
        sorted_tasks = sorted(tasks, key=lambda t: (
            priority_order.get(t.priority, 3),
            t.due_date or "9999-99-99"
        ))
        
        message = f"📋 Your {status_filter.title()} Tasks ({len(sorted_tasks)} total):\n\n"
        
        for task in sorted_tasks:
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.priority, "⚪")
            
            message += f"{priority_emoji} [{task.id}] {task.title}\n"
            
            details = []
            details.append(f"Priority: {task.priority.upper()}")
            
            if task.due_date:
                try:
                    due = datetime.fromisoformat(task.due_date)
                    days_left = (due - datetime.now()).days
                    if days_left < 0:
                        details.append(f"⚠️ OVERDUE by {abs(days_left)} days")
                    elif days_left == 0:
                        details.append("📅 Due TODAY")
                    elif days_left == 1:
                        details.append("📅 Due tomorrow")
                    else:
                        details.append(f"📅 Due in {days_left} days")
                except:
                    details.append(f"📅 Due: {task.due_date}")
            
            if task.status == "completed" and task.completed_at:
                completed = datetime.fromisoformat(task.completed_at)
                details.append(f"✅ {completed.strftime('%b %d')}")
            
            message += f"    {' | '.join(details)}\n\n"
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return SkillResult(
            success=True,
            message=message.strip(),
            data={"tasks": [t.to_dict() for t in sorted_tasks]},
            execution_time=execution_time,
            skill_name=self.name
        )
    
    def _handle_complete_task(self, user_input: str) -> SkillResult:
        """Mark a task as completed."""
        start_time = datetime.now()
        
        # Extract task ID
        task_id = self._extract_task_id(user_input)
        
        if task_id is None:
            return SkillResult(
                success=False,
                message="Please specify which task to complete. Try: 'mark task 1 as done'",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
        
        # Find task
        task = next((t for t in self.tasks if t.id == task_id), None)
        
        if not task:
            return SkillResult(
                success=False,
                message=f"I couldn't find task #{task_id}",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
        
        if task.status == "completed":
            return SkillResult(
                success=True,
                message=f"Task #{task_id} '{task.title}' is already completed! ✅",
                data={"task": task.to_dict()},
                execution_time=0.0,
                skill_name=self.name
            )
        
        # Mark as completed
        task.status = "completed"
        task.completed_at = datetime.now().isoformat()
        self._save_tasks()
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        message = f"✅ Task completed: '{task.title}'\nGreat job! 🎉"
        
        # Count remaining tasks
        remaining = len([t for t in self.tasks if t.status != "completed"])
        if remaining == 0:
            message += "\n\nAll tasks done! You're awesome! 🌟"
        else:
            message += f"\n\n{remaining} task(s) remaining."
        
        return SkillResult(
            success=True,
            message=message,
            data={"task": task.to_dict(), "remaining_tasks": remaining},
            execution_time=execution_time,
            skill_name=self.name
        )
    
    def _handle_delete_task(self, user_input: str) -> SkillResult:
        """Delete a task."""
        start_time = datetime.now()
        
        task_id = self._extract_task_id(user_input)
        
        if task_id is None:
            return SkillResult(
                success=False,
                message="Please specify which task to delete. Try: 'delete task 1'",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
        
        # Find and remove task
        task = next((t for t in self.tasks if t.id == task_id), None)
        
        if not task:
            return SkillResult(
                success=False,
                message=f"I couldn't find task #{task_id}",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
        
        self.tasks.remove(task)
        self._save_tasks()
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return SkillResult(
            success=True,
            message=f"🗑️ Task deleted: '{task.title}'",
            data={"deleted_task": task.to_dict()},
            execution_time=execution_time,
            skill_name=self.name
        )
    
    def _handle_export(self) -> SkillResult:
        """Export tasks and notes to a text file."""
        start_time = datetime.now()
        
        export_file = os.path.join(self.data_dir, f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        
        with open(export_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("JARVIS VOICE ASSISTANT - TASKS & NOTES EXPORT\n")
            f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            # Export tasks
            f.write("📋 TASKS\n")
            f.write("-" * 60 + "\n\n")
            
            if self.tasks:
                for task in sorted(self.tasks, key=lambda t: t.created_at):
                    f.write(f"[{task.id}] {task.title}\n")
                    f.write(f"    Status: {task.status.upper()}\n")
                    f.write(f"    Priority: {task.priority.upper()}\n")
                    if task.due_date:
                        f.write(f"    Due Date: {task.due_date}\n")
                    f.write(f"    Created: {task.created_at}\n")
                    if task.completed_at:
                        f.write(f"    Completed: {task.completed_at}\n")
                    f.write("\n")
            else:
                f.write("No tasks found.\n\n")
            
            # Export notes
            f.write("\n" + "=" * 60 + "\n\n")
            f.write("📝 NOTES\n")
            f.write("-" * 60 + "\n\n")
            
            if self.notes:
                for note in sorted(self.notes, key=lambda n: n.created_at):
                    f.write(f"[{note.id}] {note.content}\n")
                    f.write(f"    Category: {note.category}\n")
                    f.write(f"    Created: {note.created_at}\n\n")
            else:
                f.write("No notes found.\n")
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return SkillResult(
            success=True,
            message=f"📄 Exported to: {export_file}\n{len(self.tasks)} tasks and {len(self.notes)} notes exported!",
            data={"export_file": export_file},
            execution_time=execution_time,
            skill_name=self.name
        )
    
    # Helper methods
    
    def _load_notes(self) -> List[Note]:
        """Load notes from file."""
        if os.path.exists(self.notes_file):
            try:
                with open(self.notes_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [Note(**note) for note in data]
            except:
                return []
        return []
    
    def _load_tasks(self) -> List[Task]:
        """Load tasks from file."""
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [Task(**task) for task in data]
            except:
                return []
        return []
    
    def _save_notes(self):
        """Save notes to file."""
        with open(self.notes_file, 'w', encoding='utf-8') as f:
            json.dump([n.to_dict() for n in self.notes], f, indent=2)
    
    def _save_tasks(self):
        """Save tasks to file."""
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)
    
    def _extract_note_content(self, user_input: str) -> Optional[str]:
        """Extract note content from user input."""
        patterns = [
            r'(?:take a note|make a note|write down|jot down|save this|remember this)[:\s]+(.+)',
            r'note[:\s]+(.+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_task_title(self, user_input: str) -> Optional[str]:
        """Extract task title from user input."""
        patterns = [
            r'(?:add task|create task|new task|task)[:\s]+(.+)',
            r'(?:add|create)\s+(.+?)\s+(?:task|to do)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                # Remove priority and due date keywords
                title = re.sub(r'\s*(?:high|medium|low)\s*priority', '', title, flags=re.IGNORECASE)
                title = re.sub(r'\s*due\s+(?:today|tomorrow|in\s+\d+\s+days?)', '', title, flags=re.IGNORECASE)
                return title.strip()
        
        return None
    
    def _extract_priority(self, user_input: str) -> str:
        """Extract priority from user input."""
        if "high priority" in user_input or "urgent" in user_input or "important" in user_input:
            return "high"
        elif "low priority" in user_input:
            return "low"
        else:
            return "medium"
    
    def _extract_due_date(self, user_input: str) -> Optional[str]:
        """Extract due date from user input."""
        if "due today" in user_input or "today" in user_input:
            return datetime.now().date().isoformat()
        elif "tomorrow" in user_input:
            return (datetime.now() + timedelta(days=1)).date().isoformat()
        else:
            # Try to extract "in X days"
            match = re.search(r'in\s+(\d+)\s+days?', user_input, re.IGNORECASE)
            if match:
                days = int(match.group(1))
                return (datetime.now() + timedelta(days=days)).date().isoformat()
        
        return None
    
    def _extract_task_id(self, user_input: str) -> Optional[int]:
        """Extract task ID from user input."""
        # Look for patterns like "task 1", "task #1", "task number 1"
        match = re.search(r'task\s*#?\s*(\d+)', user_input, re.IGNORECASE)
        if match:
            return int(match.group(1))
        
        # Look for standalone numbers
        match = re.search(r'\b(\d+)\b', user_input)
        if match:
            return int(match.group(1))
        
        return None
    
    def _categorize_content(self, content: str) -> str:
        """Smart categorization based on content."""
        content_lower = content.lower()
        
        categories = {
            "work": ["meeting", "project", "report", "deadline", "presentation", "email", "call", "client"],
            "personal": ["buy", "shopping", "grocery", "clean", "laundry", "home"],
            "health": ["exercise", "workout", "gym", "doctor", "medicine", "health"],
            "finance": ["pay", "bill", "invoice", "payment", "bank", "budget"],
            "learning": ["study", "learn", "course", "read", "book", "tutorial"],
        }
        
        for category, keywords in categories.items():
            if any(keyword in content_lower for keyword in keywords):
                return category
        
        return "general"


# Skill registration
def get_skill():
    """Factory function to get the skill instance."""
    return TodoNotesSkill()

