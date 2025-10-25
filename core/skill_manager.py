"""
Skill Manager - Central component for managing and executing skills
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import time

from .skill_registry import SkillRegistry
from .priority_scheduler import PriorityScheduler
from skills.base_skill import BaseSkill, SkillContext, SkillResult


@dataclass
class SkillMetrics:
    """Metrics for skill performance tracking"""
    skill_name: str
    execution_count: int = 0
    total_execution_time: float = 0.0
    success_count: int = 0
    error_count: int = 0
    
    @property
    def average_execution_time(self) -> float:
        """Calculate average execution time"""
        return self.total_execution_time / max(self.execution_count, 1)
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage"""
        return (self.success_count / max(self.execution_count, 1)) * 100


class SkillManager:
    """Central manager for all skills in the voice assistant"""
    
    def __init__(self):
        self.skills: List[BaseSkill] = []
        self.skill_registry = SkillRegistry(self)
        self.priority_scheduler = PriorityScheduler()
        self.metrics: Dict[str, SkillMetrics] = {}
        self.execution_history: List[Dict[str, Any]] = []
        
    def register_skill(self, skill: BaseSkill) -> None:
        """Register a new skill with the manager"""
        if skill not in self.skills:
            self.skills.append(skill)
            self.skill_registry.register(skill)
            self.metrics[skill.name] = SkillMetrics(skill_name=skill.name)
            print(f"Registered skill: {skill.name}")
    
    def unregister_skill(self, skill_name: str) -> bool:
        """Unregister a skill by name"""
        for skill in self.skills[:]:
            if skill.name == skill_name:
                self.skills.remove(skill)
                self.skill_registry.unregister(skill)
                if skill_name in self.metrics:
                    del self.metrics[skill_name]
                print(f"Unregistered skill: {skill_name}")
                return True
        return False
    
    def get_skill(self, skill_name: str) -> Optional[BaseSkill]:
        """Get a skill by name"""
        for skill in self.skills:
            if skill.name == skill_name:
                return skill
        return None
    
    def list_skills(self) -> List[str]:
        """Get list of all registered skill names"""
        return [skill.name for skill in self.skills]
    
    def execute_best_skill(self, context: SkillContext) -> SkillResult:
        """Execute the best matching skill for the given context"""
        start_time = time.time()
        
        # Find skills that can handle the context
        candidate_skills = []
        for skill in self.skills:
            try:
                if skill.can_handle(context):
                    candidate_skills.append(skill)
            except Exception as e:
                print(f"Error checking skill {skill.name}: {e}")
                continue
        
        if not candidate_skills:
            return SkillResult(
                success=False,
                message="I'm sorry, I couldn't help with that. Could you please try rephrasing?",
                data={"error": "no_matching_skill"},
                execution_time=0.0,
                skill_name="skill_manager"
            )
        
        # Sort by priority
        candidate_skills.sort(key=lambda s: s.priority.value, reverse=True)
        
        # Try to execute the highest priority skill
        best_skill = candidate_skills[0]
        
        try:
            result = best_skill.execute(context)
            execution_time = time.time() - start_time
            
            # Update metrics
            self._update_metrics(best_skill.name, execution_time, result.success)
            
            # Add to execution history
            self.execution_history.append({
                "timestamp": datetime.now(),
                "skill_name": best_skill.name,
                "user_input": context.user_input,
                "success": result.success,
                "execution_time": execution_time
            })
            
            # Keep only last 100 executions
            if len(self.execution_history) > 100:
                self.execution_history = self.execution_history[-100:]
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            self._update_metrics(best_skill.name, execution_time, False)
            
            return SkillResult(
                success=False,
                message=f"Sorry, I encountered an error: {str(e)}",
                data={"error": str(e)},
                execution_time=execution_time,
                skill_name=best_skill.name,
                error=str(e)
            )
    
    def _update_metrics(self, skill_name: str, execution_time: float, success: bool) -> None:
        """Update skill performance metrics"""
        if skill_name not in self.metrics:
            self.metrics[skill_name] = SkillMetrics(skill_name=skill_name)
        
        metrics = self.metrics[skill_name]
        metrics.execution_count += 1
        metrics.total_execution_time += execution_time
        
        if success:
            metrics.success_count += 1
        else:
            metrics.error_count += 1
    
    def get_metrics(self, skill_name: Optional[str] = None) -> Dict[str, Any]:
        """Get performance metrics for skills"""
        if skill_name:
            if skill_name in self.metrics:
                metrics = self.metrics[skill_name]
                return {
                    "skill_name": metrics.skill_name,
                    "execution_count": metrics.execution_count,
                    "average_execution_time": metrics.average_execution_time,
                    "success_rate": metrics.success_rate,
                    "success_count": metrics.success_count,
                    "error_count": metrics.error_count
                }
            return {}
        
        return {name: self.get_metrics(name) for name in self.metrics.keys()}
    
    def get_execution_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent execution history"""
        return self.execution_history[-limit:] if self.execution_history else []
    
    def reset_metrics(self, skill_name: Optional[str] = None) -> None:
        """Reset metrics for a skill or all skills"""
        if skill_name and skill_name in self.metrics:
            self.metrics[skill_name] = SkillMetrics(skill_name=skill_name)
        elif not skill_name:
            self.metrics.clear()
            for skill in self.skills:
                self.metrics[skill.name] = SkillMetrics(skill_name=skill.name)
    
    def get_skill_statistics(self) -> Dict[str, Any]:
        """Get overall skill statistics"""
        total_executions = sum(metrics.execution_count for metrics in self.metrics.values())
        total_successes = sum(metrics.success_count for metrics in self.metrics.values())
        total_errors = sum(metrics.error_count for metrics in self.metrics.values())
        
        return {
            "total_skills": len(self.skills),
            "total_executions": total_executions,
            "total_successes": total_successes,
            "total_errors": total_errors,
            "overall_success_rate": (total_successes / max(total_executions, 1)) * 100,
            "skills": list(self.metrics.keys())
        }
