"""
Skill Registry - Manages skill registration and discovery
"""

from typing import List, Dict, Set, Optional
from skills.base_skill import BaseSkill, SkillPriority


class SkillRegistry:
    """Registry for managing skill registration and discovery"""
    
    def __init__(self, skill_manager):
        self.skill_manager = skill_manager
        self.skills_by_priority: Dict[SkillPriority, List[BaseSkill]] = {
            priority: [] for priority in SkillPriority
        }
        self.skills_by_name: Dict[str, BaseSkill] = {}
        self.skill_keywords: Dict[str, Set[str]] = {}
    
    def register(self, skill: BaseSkill) -> None:
        """Register a skill in the registry"""
        # Add to priority-based registry
        self.skills_by_priority[skill.priority].append(skill)
        
        # Add to name-based registry
        self.skills_by_name[skill.name] = skill
        
        # Extract keywords for the skill
        self._extract_keywords(skill)
    
    def unregister(self, skill: BaseSkill) -> None:
        """Unregister a skill from the registry"""
        # Remove from priority-based registry
        if skill in self.skills_by_priority[skill.priority]:
            self.skills_by_priority[skill.priority].remove(skill)
        
        # Remove from name-based registry
        if skill.name in self.skills_by_name:
            del self.skills_by_name[skill.name]
        
        # Remove keywords
        if skill.name in self.skill_keywords:
            del self.skill_keywords[skill.name]
    
    def get_skills_by_priority(self, priority: SkillPriority) -> List[BaseSkill]:
        """Get all skills with a specific priority"""
        return self.skills_by_priority[priority].copy()
    
    def get_skill_by_name(self, name: str) -> Optional[BaseSkill]:
        """Get a skill by its name"""
        return self.skill_keywords.get(name)
    
    def get_all_skills(self) -> List[BaseSkill]:
        """Get all registered skills"""
        return list(self.skills_by_name.values())
    
    def get_skills_by_keyword(self, keyword: str) -> List[BaseSkill]:
        """Get skills that contain a specific keyword"""
        matching_skills = []
        for skill_name, keywords in self.skill_keywords.items():
            if keyword.lower() in keywords:
                skill = self.skills_by_name.get(skill_name)
                if skill:
                    matching_skills.append(skill)
        return matching_skills
    
    def search_skills(self, query: str) -> List[BaseSkill]:
        """Search for skills based on a query string"""
        query_lower = query.lower()
        matching_skills = []
        
        for skill in self.get_all_skills():
            # Check if skill name contains query
            if query_lower in skill.name.lower():
                matching_skills.append(skill)
                continue
            
            # Check if any keywords match
            if skill.name in self.skill_keywords:
                keywords = self.skill_keywords[skill.name]
                if any(query_lower in keyword for keyword in keywords):
                    matching_skills.append(skill)
        
        return matching_skills
    
    def get_skill_info(self, skill_name: str) -> Optional[Dict[str, any]]:
        """Get detailed information about a skill"""
        skill = self.skills_by_name.get(skill_name)
        if not skill:
            return None
        
        return {
            "name": skill.name,
            "priority": skill.priority.name,
            "keywords": list(self.skill_keywords.get(skill_name, set())),
            "description": getattr(skill, 'description', 'No description available'),
            "version": getattr(skill, 'version', '1.0.0')
        }
    
    def get_registry_stats(self) -> Dict[str, any]:
        """Get statistics about the skill registry"""
        total_skills = len(self.skills_by_name)
        skills_by_priority_count = {
            priority.name: len(skills) 
            for priority, skills in self.skills_by_priority.items()
        }
        
        total_keywords = sum(len(keywords) for keywords in self.skill_keywords.values())
        
        return {
            "total_skills": total_skills,
            "skills_by_priority": skills_by_priority_count,
            "total_keywords": total_keywords,
            "skill_names": list(self.skills_by_name.keys())
        }
    
    def _extract_keywords(self, skill: BaseSkill) -> None:
        """Extract keywords from a skill for better searchability"""
        keywords = set()
        
        # Add skill name as keyword
        keywords.add(skill.name.lower())
        
        # Try to extract keywords from skill attributes
        if hasattr(skill, 'keywords'):
            if isinstance(skill.keywords, (list, tuple)):
                keywords.update([kw.lower() for kw in skill.keywords])
            elif isinstance(skill.keywords, str):
                keywords.add(skill.keywords.lower())
        
        # Try to extract keywords from skill description
        if hasattr(skill, 'description'):
            description_words = skill.description.lower().split()
            # Add meaningful words (longer than 2 characters)
            keywords.update([word for word in description_words if len(word) > 2])
        
        # Add priority as keyword
        keywords.add(skill.priority.name.lower())
        
        self.skill_keywords[skill.name] = keywords
    
    def clear(self) -> None:
        """Clear all registered skills"""
        self.skills_by_priority.clear()
        self.skills_by_name.clear()
        self.skill_keywords.clear()
        
        # Reinitialize priority dictionary
        for priority in SkillPriority:
            self.skills_by_priority[priority] = []
