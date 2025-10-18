"""
Base skill class and skill management framework.
Demonstrates plugin architecture, dependency injection, and extensibility patterns.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable, Type
from dataclasses import dataclass
from enum import Enum
import threading
import time
import inspect
from collections import defaultdict


class SkillPriority(Enum):
    """Skill execution priority levels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class SkillStatus(Enum):
    """Skill execution status."""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class SkillContext:
    """Context data passed to skills during execution."""
    user_input: str
    intent: str
    entities: Dict[str, Any]
    confidence: float
    session_id: str
    user_id: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class SkillResult:
    """Result of skill execution."""
    success: bool
    message: str
    data: Dict[str, Any]
    execution_time: float
    skill_name: str
    error: Optional[str] = None


class BaseSkill(ABC):
    """
    Abstract base class for all voice assistant skills.
    Demonstrates the Template Method pattern and plugin architecture.
    """
    
    def __init__(self, name: str, description: str = "", priority: SkillPriority = SkillPriority.NORMAL):
        self.name = name
        self.description = description
        self.priority = priority
        self.status = SkillStatus.IDLE
        self.dependencies: List[str] = []
        self.required_entities: List[str] = []
        self.optional_entities: List[str] = []
        self.triggers: List[str] = []
        self.callbacks: List[Callable] = []
        self.execution_count = 0
        self.total_execution_time = 0.0
        self.last_execution_time = 0.0
        self.lock = threading.RLock()
    
    @abstractmethod
    def can_handle(self, context: SkillContext) -> bool:
        """
        Determine if this skill can handle the given context.
        This is the primary method for skill selection.
        """
        pass
    
    @abstractmethod
    def execute(self, context: SkillContext) -> SkillResult:
        """
        Execute the skill with the given context.
        This is where the main skill logic is implemented.
        """
        pass
    
    def pre_execute(self, context: SkillContext) -> bool:
        """
        Pre-execution validation and setup.
        Return False to prevent execution.
        """
        return True
    
    def post_execute(self, context: SkillContext, result: SkillResult) -> None:
        """
        Post-execution cleanup and logging.
        Called after skill execution regardless of success/failure.
        """
        pass
    
    def handle_error(self, context: SkillContext, error: Exception) -> SkillResult:
        """
        Handle errors that occur during skill execution.
        Override for custom error handling.
        """
        return SkillResult(
            success=False,
            message=f"Error in {self.name}: {str(error)}",
            data={},
            execution_time=0.0,
            skill_name=self.name,
            error=str(error)
        )
    
    def add_callback(self, callback: Callable[[str, Dict], None]) -> None:
        """Add callback for skill events."""
        self.callbacks.append(callback)
    
    def _notify_callbacks(self, event: str, data: Dict[str, Any]) -> None:
        """Notify all callbacks of an event."""
        for callback in self.callbacks:
            try:
                callback(event, data)
            except Exception as e:
                print(f"Error in skill callback: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get skill execution statistics."""
        with self.lock:
            avg_execution_time = (self.total_execution_time / self.execution_count 
                                if self.execution_count > 0 else 0.0)
            
            return {
                'name': self.name,
                'description': self.description,
                'priority': self.priority.value,
                'status': self.status.value,
                'execution_count': self.execution_count,
                'total_execution_time': self.total_execution_time,
                'average_execution_time': avg_execution_time,
                'last_execution_time': self.last_execution_time,
                'dependencies': self.dependencies,
                'required_entities': self.required_entities,
                'optional_entities': self.optional_entities,
                'triggers': self.triggers
            }


class SkillManager:
    """
    Manages skill registration, selection, and execution.
    Demonstrates the Strategy pattern and dependency management.
    """
    
    def __init__(self):
        self.skills: Dict[str, BaseSkill] = {}
        self.skill_dependencies: Dict[str, List[str]] = defaultdict(list)
        self.execution_history: List[Dict] = []
        self.lock = threading.RLock()
    
    def register_skill(self, skill: BaseSkill) -> bool:
        """Register a new skill."""
        with self.lock:
            if skill.name in self.skills:
                print(f"Skill '{skill.name}' is already registered")
                return False
            
            # Validate dependencies
            if not self._validate_dependencies(skill):
                print(f"Skill '{skill.name}' has invalid dependencies")
                return False
            
            self.skills[skill.name] = skill
            self.skill_dependencies[skill.name] = skill.dependencies.copy()
            
            print(f"Registered skill: {skill.name}")
            return True
    
    def unregister_skill(self, skill_name: str) -> bool:
        """Unregister a skill."""
        with self.lock:
            if skill_name not in self.skills:
                return False
            
            # Check if other skills depend on this one
            dependent_skills = [name for name, deps in self.skill_dependencies.items() 
                              if skill_name in deps]
            
            if dependent_skills:
                print(f"Cannot unregister '{skill_name}': {dependent_skills} depend on it")
                return False
            
            del self.skills[skill_name]
            del self.skill_dependencies[skill_name]
            
            print(f"Unregistered skill: {skill_name}")
            return True
    
    def get_skill(self, skill_name: str) -> Optional[BaseSkill]:
        """Get a skill by name."""
        with self.lock:
            return self.skills.get(skill_name)
    
    def find_skills_for_context(self, context: SkillContext) -> List[BaseSkill]:
        """Find skills that can handle the given context."""
        with self.lock:
            candidate_skills = []
            
            for skill in self.skills.values():
                try:
                    if skill.can_handle(context):
                        candidate_skills.append(skill)
                except Exception as e:
                    print(f"Error checking skill '{skill.name}': {e}")
            
            # Sort by priority (higher priority first)
            candidate_skills.sort(key=lambda s: s.priority.value, reverse=True)
            
            return candidate_skills
    
    def execute_skill(self, skill_name: str, context: SkillContext) -> SkillResult:
        """Execute a specific skill."""
        skill = self.get_skill(skill_name)
        if not skill:
            return SkillResult(
                success=False,
                message=f"Skill '{skill_name}' not found",
                data={},
                execution_time=0.0,
                skill_name=skill_name,
                error="Skill not found"
            )
        
        return self._execute_skill_internal(skill, context)
    
    def execute_best_skill(self, context: SkillContext) -> SkillResult:
        """Execute the best skill for the given context."""
        candidate_skills = self.find_skills_for_context(context)
        
        if not candidate_skills:
            return SkillResult(
                success=False,
                message="No suitable skill found",
                data={},
                execution_time=0.0,
                skill_name="none",
                error="No suitable skill"
            )
        
        # Try skills in priority order
        for skill in candidate_skills:
            try:
                result = self._execute_skill_internal(skill, context)
                if result.success:
                    return result
            except Exception as e:
                print(f"Error executing skill '{skill.name}': {e}")
                continue
        
        # If no skill succeeded, return failure
        return SkillResult(
            success=False,
            message="All candidate skills failed",
            data={},
            execution_time=0.0,
            skill_name="multiple",
            error="All skills failed"
        )
    
    def _execute_skill_internal(self, skill: BaseSkill, context: SkillContext) -> SkillResult:
        """Internal skill execution with timing and error handling."""
        start_time = time.time()
        
        with skill.lock:
            skill.status = SkillStatus.RUNNING
            skill._notify_callbacks('skill_started', {'skill_name': skill.name, 'context': context})
        
        try:
            # Pre-execution validation
            if not skill.pre_execute(context):
                result = SkillResult(
                    success=False,
                    message=f"Pre-execution validation failed for {skill.name}",
                    data={},
                    execution_time=0.0,
                    skill_name=skill.name,
                    error="Pre-execution validation failed"
                )
            else:
                # Execute the skill
                result = skill.execute(context)
            
            # Update statistics
            execution_time = time.time() - start_time
            result.execution_time = execution_time
            
            with skill.lock:
                skill.execution_count += 1
                skill.total_execution_time += execution_time
                skill.last_execution_time = execution_time
                skill.status = SkillStatus.COMPLETED if result.success else SkillStatus.FAILED
            
            # Post-execution cleanup
            skill.post_execute(context, result)
            
            # Record execution
            self._record_execution(skill, context, result)
            
            # Notify callbacks
            skill._notify_callbacks('skill_completed', {
                'skill_name': skill.name,
                'result': result,
                'context': context
            })
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            with skill.lock:
                skill.status = SkillStatus.FAILED
            
            result = skill.handle_error(context, e)
            result.execution_time = execution_time
            
            # Record failed execution
            self._record_execution(skill, context, result)
            
            # Notify callbacks
            skill._notify_callbacks('skill_failed', {
                'skill_name': skill.name,
                'error': str(e),
                'context': context
            })
            
            return result
    
    def _validate_dependencies(self, skill: BaseSkill) -> bool:
        """Validate that all skill dependencies are available."""
        for dep in skill.dependencies:
            if dep not in self.skills:
                return False
        return True
    
    def _record_execution(self, skill: BaseSkill, context: SkillContext, result: SkillResult) -> None:
        """Record skill execution in history."""
        with self.lock:
            self.execution_history.append({
                'timestamp': time.time(),
                'skill_name': skill.name,
                'context': context,
                'result': result
            })
            
            # Keep only last 1000 executions
            if len(self.execution_history) > 1000:
                self.execution_history = self.execution_history[-1000:]
    
    def get_skill_statistics(self) -> Dict[str, Any]:
        """Get statistics for all skills."""
        with self.lock:
            stats = {}
            for skill in self.skills.values():
                stats[skill.name] = skill.get_statistics()
            return stats
    
    def get_execution_history(self, limit: int = 100) -> List[Dict]:
        """Get recent execution history."""
        with self.lock:
            return self.execution_history[-limit:]
    
    def get_skills_by_priority(self) -> Dict[int, List[str]]:
        """Get skills grouped by priority."""
        with self.lock:
            by_priority = defaultdict(list)
            for skill in self.skills.values():
                by_priority[skill.priority.value].append(skill.name)
            return dict(by_priority)


class SkillRegistry:
    """
    Skill registry for automatic skill discovery and registration.
    Demonstrates reflection and plugin loading.
    """
    
    def __init__(self, skill_manager: SkillManager):
        self.skill_manager = skill_manager
        self.registered_modules = set()
    
    def register_skill_class(self, skill_class: Type[BaseSkill], *args, **kwargs) -> bool:
        """Register a skill class by instantiating it."""
        try:
            skill_instance = skill_class(*args, **kwargs)
            return self.skill_manager.register_skill(skill_instance)
        except Exception as e:
            print(f"Error registering skill class {skill_class.__name__}: {e}")
            return False
    
    def register_skill_instance(self, skill_instance: BaseSkill) -> bool:
        """Register a skill instance."""
        return self.skill_manager.register_skill(skill_instance)
    
    def discover_skills_in_module(self, module) -> int:
        """Discover and register all skill classes in a module."""
        registered_count = 0
        
        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and 
                issubclass(obj, BaseSkill) and 
                obj != BaseSkill):
                try:
                    skill_instance = obj()
                    if self.skill_manager.register_skill(skill_instance):
                        registered_count += 1
                except Exception as e:
                    print(f"Error instantiating skill {name}: {e}")
        
        return registered_count


if __name__ == "__main__":
    # Demo the skill framework
    class DemoSkill(BaseSkill):
        def __init__(self):
            super().__init__("demo", "A demonstration skill", SkillPriority.NORMAL)
            self.triggers = ["demo", "test"]
        
        def can_handle(self, context: SkillContext) -> bool:
            return any(trigger in context.user_input.lower() for trigger in self.triggers)
        
        def execute(self, context: SkillContext) -> SkillResult:
            return SkillResult(
                success=True,
                message="Demo skill executed successfully!",
                data={"input": context.user_input},
                execution_time=0.0,
                skill_name=self.name
            )
    
    # Create skill manager
    manager = SkillManager()
    
    # Register demo skill
    demo_skill = DemoSkill()
    manager.register_skill(demo_skill)
    
    # Create test context
    context = SkillContext(
        user_input="This is a demo test",
        intent="demo",
        entities={},
        confidence=0.9,
        session_id="test_session"
    )
    
    # Execute skill
    result = manager.execute_best_skill(context)
    print(f"Execution result: {result}")
    
    # Show statistics
    stats = manager.get_skill_statistics()
    print(f"Skill statistics: {stats}")




