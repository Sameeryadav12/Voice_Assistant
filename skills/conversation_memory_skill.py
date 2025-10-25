"""
Conversation Memory & Context Skill - Intelligent conversation management
Provides context-aware responses and conversation memory.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from skills.base_skill import BaseSkill, SkillContext, SkillResult, SkillPriority
from dataclasses import dataclass, asdict
import re


@dataclass
class ConversationTurn:
    """Represents a single conversation turn."""
    timestamp: str
    user_input: str
    assistant_response: str
    intent: str
    entities: Dict[str, Any]


@dataclass
class UserProfile:
    """Represents user preferences and history."""
    user_id: str
    name: Optional[str] = None
    preferences: Dict[str, Any] = None
    conversation_history: List[Dict] = None
    last_interaction: Optional[str] = None
    
    def __post_init__(self):
        if self.preferences is None:
            self.preferences = {}
        if self.conversation_history is None:
            self.conversation_history = []


class ConversationMemorySkill(BaseSkill):
    """
    Advanced skill for conversation memory and context awareness.
    Features:
    - Remember previous conversations
    - Context-aware responses
    - User preferences
    - Smart follow-ups
    - Conversation history
    """
    
    def __init__(self):
        super().__init__(
            name="conversation_memory",
            description="Remember conversations and provide context-aware responses",
            priority=SkillPriority.NORMAL  # Lower priority, more of a support skill
        )
        
        # Storage paths
        self.data_dir = "data"
        self.memory_file = os.path.join(self.data_dir, "conversation_memory.json")
        self.profile_file = os.path.join(self.data_dir, "user_profile.json")
        
        # Create data directory
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Load data
        self.conversation_history = self._load_conversation_history()
        self.user_profile = self._load_user_profile()
        
        # Context window (last N turns)
        self.context_window = 5
        
    def can_handle(self, context: SkillContext) -> bool:
        """Check if this skill can handle the request."""
        user_input = context.user_input.lower()
        
        # Memory/recall keywords
        memory_keywords = [
            "remember", "what did i", "did i say", "do you remember",
            "what did we talk", "what did we discuss", "what we talked",
            "last time", "earlier", "before", "previous", "my name",
            "who am i", "tell me about", "what do you know",
            "conversation history", "what we said", "our conversation"
        ]
        
        # Context-dependent queries
        context_keywords = [
            "what about", "and also", "tell me more", "continue",
            "more about that", "about that", "expand on"
        ]
        
        has_memory = any(keyword in user_input for keyword in memory_keywords)
        has_context = any(keyword in user_input for keyword in context_keywords)
        
        return has_memory or has_context
    
    def execute(self, context: SkillContext) -> SkillResult:
        """Execute memory/context command."""
        user_input = context.user_input.lower()
        
        try:
            # Handle name queries
            if "my name" in user_input or "who am i" in user_input:
                return self._handle_name_query()
            
            # Handle memory recall
            elif any(word in user_input for word in ["what did i", "did i say", "do you remember", "last time"]):
                return self._handle_memory_recall(user_input)
            
            # Handle conversation history
            elif "conversation history" in user_input or "what did we talk about" in user_input:
                return self._handle_conversation_history()
            
            # Handle context continuation
            elif any(word in user_input for word in ["more about", "tell me more", "continue", "expand"]):
                return self._handle_context_continuation()
            
            # Handle profile info
            elif "what do you know" in user_input or "tell me about me" in user_input:
                return self._handle_profile_info()
            
            else:
                return SkillResult(
                    success=False,
                    message="I can remember our conversations! Ask me 'what did we talk about?' or 'do you remember...'",
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
    
    def add_conversation_turn(self, user_input: str, assistant_response: str, 
                            intent: str = "unknown", entities: Dict = None):
        """Add a conversation turn to memory (called by main app)."""
        if entities is None:
            entities = {}
        
        turn = ConversationTurn(
            timestamp=datetime.now().isoformat(),
            user_input=user_input,
            assistant_response=assistant_response,
            intent=intent,
            entities=entities
        )
        
        self.conversation_history.append(asdict(turn))
        
        # Keep only recent history (last 100 turns)
        if len(self.conversation_history) > 100:
            self.conversation_history = self.conversation_history[-100:]
        
        self._save_conversation_history()
        
        # Update user profile
        self.user_profile.last_interaction = datetime.now().isoformat()
        self._save_user_profile()
    
    def get_recent_context(self, n: int = 5) -> List[Dict]:
        """Get recent conversation context."""
        return self.conversation_history[-n:] if self.conversation_history else []
    
    def _handle_name_query(self) -> SkillResult:
        """Handle queries about user's name."""
        if self.user_profile.name:
            message = f"Your name is {self.user_profile.name}! 😊"
        else:
            message = "I don't know your name yet! You can tell me by saying 'my name is [your name]'"
        
        return SkillResult(
            success=True,
            message=message,
            data={"name": self.user_profile.name},
            execution_time=0.0,
            skill_name=self.name
        )
    
    def _handle_memory_recall(self, user_input: str) -> SkillResult:
        """Handle memory recall queries."""
        if not self.conversation_history:
            return SkillResult(
                success=True,
                message="This is our first conversation! I don't have any memory yet.",
                data={"history": []},
                execution_time=0.0,
                skill_name=self.name
            )
        
        # Try to find relevant past conversations
        query_keywords = self._extract_keywords(user_input)
        
        relevant_turns = []
        for turn in reversed(self.conversation_history[-20:]):  # Check last 20 turns
            turn_text = f"{turn['user_input']} {turn['assistant_response']}".lower()
            if any(keyword in turn_text for keyword in query_keywords):
                relevant_turns.append(turn)
            
            if len(relevant_turns) >= 3:
                break
        
        if relevant_turns:
            message = "🧠 Here's what I remember:\n\n"
            for i, turn in enumerate(reversed(relevant_turns), 1):
                timestamp = datetime.fromisoformat(turn['timestamp'])
                time_str = timestamp.strftime("%b %d, %I:%M %p")
                message += f"{i}. [{time_str}]\n"
                message += f"   You: {turn['user_input']}\n"
                message += f"   Me: {turn['assistant_response'][:100]}...\n\n"
        else:
            message = "🤔 I don't recall discussing that topic recently. Could you be more specific?"
        
        return SkillResult(
            success=True,
            message=message.strip(),
            data={"relevant_turns": relevant_turns},
            execution_time=0.0,
            skill_name=self.name
        )
    
    def _handle_conversation_history(self) -> SkillResult:
        """Handle conversation history queries."""
        if not self.conversation_history:
            return SkillResult(
                success=True,
                message="This is our first conversation!",
                data={"history": []},
                execution_time=0.0,
                skill_name=self.name
            )
        
        recent_turns = self.conversation_history[-5:]
        
        message = f"📜 Recent Conversation ({len(recent_turns)} turns):\n\n"
        
        for i, turn in enumerate(recent_turns, 1):
            timestamp = datetime.fromisoformat(turn['timestamp'])
            time_str = timestamp.strftime("%I:%M %p")
            message += f"{i}. [{time_str}] You: {turn['user_input']}\n"
            response = turn['assistant_response'][:80] + "..." if len(turn['assistant_response']) > 80 else turn['assistant_response']
            message += f"   Me: {response}\n\n"
        
        total_conversations = len(self.conversation_history)
        if total_conversations > 5:
            message += f"\n💬 Total conversations: {total_conversations}"
        
        return SkillResult(
            success=True,
            message=message.strip(),
            data={"history": recent_turns},
            execution_time=0.0,
            skill_name=self.name
        )
    
    def _handle_context_continuation(self) -> SkillResult:
        """Handle context continuation queries."""
        if not self.conversation_history:
            return SkillResult(
                success=False,
                message="I don't have any previous context to continue from.",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
        
        last_turn = self.conversation_history[-1]
        
        message = f"🔗 Continuing from our last topic:\n\n"
        message += f"You asked: '{last_turn['user_input']}'\n"
        message += f"I said: '{last_turn['assistant_response']}'\n\n"
        message += "What would you like to know more about?"
        
        return SkillResult(
            success=True,
            message=message,
            data={"last_turn": last_turn},
            execution_time=0.0,
            skill_name=self.name
        )
    
    def _handle_profile_info(self) -> SkillResult:
        """Handle user profile information queries."""
        if not self.user_profile.name and not self.user_profile.preferences:
            message = "I don't have much information about you yet! As we chat more, I'll learn your preferences."
        else:
            message = "👤 What I know about you:\n\n"
            
            if self.user_profile.name:
                message += f"Name: {self.user_profile.name}\n"
            
            if self.conversation_history:
                message += f"Conversations: {len(self.conversation_history)}\n"
            
            if self.user_profile.last_interaction:
                last_time = datetime.fromisoformat(self.user_profile.last_interaction)
                message += f"Last interaction: {last_time.strftime('%b %d, %I:%M %p')}\n"
            
            if self.user_profile.preferences:
                message += f"\nPreferences: {len(self.user_profile.preferences)} saved"
        
        return SkillResult(
            success=True,
            message=message,
            data={"profile": asdict(self.user_profile)},
            execution_time=0.0,
            skill_name=self.name
        )
    
    def set_user_name(self, name: str):
        """Set user's name."""
        self.user_profile.name = name
        self._save_user_profile()
    
    def set_preference(self, key: str, value: Any):
        """Set a user preference."""
        self.user_profile.preferences[key] = value
        self._save_user_profile()
    
    def get_preference(self, key: str) -> Optional[Any]:
        """Get a user preference."""
        return self.user_profile.preferences.get(key)
    
    # Helper methods
    
    def _load_conversation_history(self) -> List[Dict]:
        """Load conversation history from file."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _load_user_profile(self) -> UserProfile:
        """Load user profile from file."""
        if os.path.exists(self.profile_file):
            try:
                with open(self.profile_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return UserProfile(**data)
            except:
                return UserProfile(user_id="default_user")
        return UserProfile(user_id="default_user")
    
    def _save_conversation_history(self):
        """Save conversation history to file."""
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, indent=2)
    
    def _save_user_profile(self):
        """Save user profile to file."""
        with open(self.profile_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.user_profile), f, indent=2)
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text for memory search."""
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'what',
                     'did', 'i', 'you', 'me', 'my', 'your', 'we', 'us', 'do', 'does'}
        
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [w for w in words if w not in stop_words and len(w) > 3]
        
        return keywords[:5]  # Return top 5 keywords


# Skill registration
def get_skill():
    """Factory function to get the skill instance."""
    return ConversationMemorySkill()

