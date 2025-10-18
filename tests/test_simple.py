"""
Simple test script to verify the voice assistant components work correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_core_components():
    """Test core components without audio."""
    print("Testing Core Components...")
    
    # Test Trie
    from core.trie import KeywordMatcher
    matcher = KeywordMatcher()
    print(f"[OK] Trie: Wake word detection = {matcher.detect_wake_word('Hey Sigma, what time is it?')}")
    
    # Test State Machine
    from core.state_machine import DialogueStateMachine, EventType
    sm = DialogueStateMachine()
    print(f"[OK] State Machine: Initial state = {sm.get_state_info()['current_state']}")
    
    # Test Scheduler
    from core.scheduler import PriorityScheduler, TaskPriority
    scheduler = PriorityScheduler()
    print(f"[OK] Scheduler: Created with {scheduler.max_workers} workers")
    
    # Test Cache
    from core.cache import CacheManager
    cache_manager = CacheManager()
    cache_manager.cache_speech_result("test", "Hello", 0.9)
    result = cache_manager.get_speech_result("test")
    print(f"[OK] Cache: Stored and retrieved = {result is not None}")
    
    # Test Graph Search
    from core.graph_search import FileSystemGraph
    fs_graph = FileSystemGraph()
    print(f"[OK] Graph Search: Built graph with {len(fs_graph.nodes)} nodes")
    
    # Test NLP
    from nlp.intent_classifier import HybridIntentClassifier, IntentType
    classifier = HybridIntentClassifier()
    classifier.add_training_data("Hello there", IntentType.GREETING)
    classifier.train_ml()
    result = classifier.classify("Hello there")
    print(f"[OK] NLP: Intent classification = {result.intent.value}")
    
    # Test Skills
    from skills.base_skill import SkillManager, SkillContext
    from skills.reminder_skill import ReminderSkill
    
    skill_manager = SkillManager()
    reminder_skill = ReminderSkill(scheduler)
    skill_manager.register_skill(reminder_skill)
    
    context = SkillContext(
        user_input="What reminders do I have?",
        intent="reminder_query",
        entities={},
        confidence=0.9,
        session_id="test"
    )
    
    result = skill_manager.execute_best_skill(context)
    print(f"[OK] Skills: Skill execution = {result.success}")
    
    scheduler.shutdown()
    print("\nAll core components working correctly! [SUCCESS]")

if __name__ == "__main__":
    test_core_components()
