"""
Demo script for Sigma Voice Assistant.
This script demonstrates the core algorithms and data structures without the full UI.
"""

import sys
import os
import time
from typing import Dict, Any

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def demo_trie_algorithm():
    """Demonstrate Trie-based keyword matching."""
    print("=" * 60)
    print("DEMO: Trie-based Keyword Matching Algorithm")
    print("=" * 60)
    
    from core.trie import AdvancedTrie, KeywordMatcher
    
    # Create trie and add words
    trie = AdvancedTrie()
    words = ["hello", "world", "python", "algorithm", "data", "structure", "voice", "assistant"]
    
    print("Adding words to trie:")
    for word in words:
        trie.insert(word, {"type": "demo", "frequency": 1})
        print(f"  Added: {word}")
    
    print(f"\nTrie size: {trie.size}")
    
    # Test exact search
    print("\nTesting exact search:")
    test_words = ["hello", "python", "nonexistent"]
    for word in test_words:
        found = trie.search_exact(word)
        print(f"  '{word}': {'Found' if found else 'Not found'}")
    
    # Test fuzzy search
    print("\nTesting fuzzy search:")
    fuzzy_queries = ["helo", "pythn", "algoritm"]
    for query in fuzzy_queries:
        results = trie.search_fuzzy(query, max_distance=2)
        print(f"  '{query}': {[r[0] for r in results[:3]]}")
    
    # Test keyword matcher
    print("\nTesting keyword matcher:")
    matcher = KeywordMatcher()
    test_phrases = [
        "Hey Sigma, what time is it?",
        "Hello world",
        "Set a reminder for 3pm"
    ]
    
    for phrase in test_phrases:
        wake_detected = matcher.detect_wake_word(phrase)
        intent = matcher.extract_intent(phrase)
        print(f"  '{phrase}'")
        print(f"    Wake word: {wake_detected}")
        print(f"    Intent: {intent}")
    
    print("\n" + "=" * 60)


def demo_state_machine():
    """Demonstrate Finite State Machine."""
    print("DEMO: Finite State Machine for Dialogue Management")
    print("=" * 60)
    
    from core.state_machine import DialogueStateMachine, EventType
    
    sm = DialogueStateMachine()
    
    print("Initial state:", sm.get_state_info()['current_state'])
    
    # Simulate conversation flow
    events = [
        (EventType.WAKE_WORD_DETECTED, {"user_input": "Hey Sigma"}),
        (EventType.SPEECH_RECOGNIZED, {"recognized_text": "What time is it?"}),
        (EventType.INTENT_CLASSIFIED, {"intent": "time_query", "confidence": 0.9}),
        (EventType.RESPONSE_READY, {"response": "It's 3:30 PM"}),
    ]
    
    print("\nSimulating conversation flow:")
    for event, data in events:
        print(f"\nProcessing event: {event.value}")
        sm.process_event(event, data)
        state_info = sm.get_state_info()
        print(f"Current state: {state_info['current_state']}")
        print(f"Context: {state_info['context']}")
    
    print("\n" + "=" * 60)


def demo_scheduler():
    """Demonstrate Priority Heap-based Scheduler."""
    print("DEMO: Priority Heap-based Task Scheduler")
    print("=" * 60)
    
    from core.scheduler import PriorityScheduler, TaskPriority, ReminderManager
    
    scheduler = PriorityScheduler(max_workers=2)
    reminder_manager = ReminderManager(scheduler)
    
    print("Scheduling tasks with different priorities:")
    
    # Schedule some test tasks
    def test_task(name: str, duration: float = 0.5):
        print(f"  Executing task: {name}")
        time.sleep(duration)
        print(f"  Completed task: {name}")
    
    # Schedule tasks with different priorities and delays
    scheduler.schedule_task(
        test_task, 
        args=("High Priority Task", 0.3), 
        delay=0.5, 
        priority=TaskPriority.HIGH
    )
    scheduler.schedule_task(
        test_task, 
        args=("Low Priority Task", 0.3), 
        delay=0.2, 
        priority=TaskPriority.LOW
    )
    scheduler.schedule_task(
        test_task, 
        args=("Normal Priority Task", 0.3), 
        delay=0.0, 
        priority=TaskPriority.NORMAL
    )
    
    # Set some reminders
    current_time = time.time()
    reminder_manager.set_reminder("Call mom", current_time + 2.0)
    reminder_manager.set_reminder("Buy groceries", current_time + 3.0, TaskPriority.HIGH)
    
    print(f"\nScheduler statistics: {scheduler.get_statistics()}")
    print(f"Upcoming reminders: {len(reminder_manager.get_upcoming_reminders())}")
    
    # Let it run for a bit
    print("\nRunning tasks...")
    time.sleep(5)
    
    print(f"\nFinal statistics: {scheduler.get_statistics()}")
    scheduler.shutdown()
    
    print("\n" + "=" * 60)


def demo_cache():
    """Demonstrate LRU Cache System."""
    print("DEMO: LRU Cache System")
    print("=" * 60)
    
    from core.cache import AdvancedLRUCache, CacheManager
    
    # Test basic LRU cache
    cache = AdvancedLRUCache(max_size=5, max_memory_mb=10)
    
    print("Testing LRU cache with size limit 5:")
    
    # Add items
    for i in range(7):
        cache.put(f"key_{i}", f"value_{i}")
        print(f"  Added key_{i}, cache size: {len(cache.cache)}")
    
    # Test access pattern
    print("\nTesting access pattern (key_2, key_4, key_6):")
    for key in ["key_2", "key_4", "key_6"]:
        value = cache.get(key)
        print(f"  {key}: {value}")
    
    # Add more items to trigger eviction
    print("\nAdding more items to trigger eviction:")
    for i in range(7, 10):
        cache.put(f"key_{i}", f"value_{i}")
        print(f"  Added key_{i}, cache size: {len(cache.cache)}")
    
    print(f"\nCache statistics: {cache.get_statistics()}")
    
    # Test cache manager
    print("\nTesting Cache Manager:")
    cache_manager = CacheManager()
    
    # Cache some data
    cache_manager.cache_speech_result("audio_hash_123", "Hello world", 0.95)
    cache_manager.cache_intent_result("What time is it?", "time_query", 0.9)
    cache_manager.cache_response("What time is it?", "It's 3:30 PM")
    
    # Retrieve cached data
    speech_result = cache_manager.get_speech_result("audio_hash_123")
    intent_result = cache_manager.get_intent_result("What time is it?")
    response = cache_manager.get_response("What time is it?")
    
    print(f"  Speech result: {speech_result}")
    print(f"  Intent result: {intent_result}")
    print(f"  Response: {response}")
    
    print(f"\nAll cache statistics: {cache_manager.get_all_statistics()}")
    
    print("\n" + "=" * 60)


def demo_graph_search():
    """Demonstrate Graph-based Search Algorithms."""
    print("DEMO: Graph-based Search Algorithms")
    print("=" * 60)
    
    from core.graph_search import FileSystemGraph, ApplicationLauncher
    
    # Create file system graph (limited scope for demo)
    print("Building file system graph...")
    fs_graph = FileSystemGraph()
    
    stats = fs_graph.get_statistics()
    print(f"Graph statistics: {stats}")
    
    # Test search functionality
    print("\nTesting file search:")
    search_queries = ["*.py", "*.txt", "README"]
    
    for query in search_queries:
        results = fs_graph.search_by_name(query, max_results=3)
        print(f"  Search '{query}': {len(results)} results")
        for result in results[:2]:  # Show first 2 results
            print(f"    - {result.name} at {result.path}")
    
    # Test application launcher
    print("\nTesting application launcher:")
    launcher = ApplicationLauncher(fs_graph)
    
    app_queries = ["calculator", "notepad", "browser"]
    for app in app_queries:
        apps = launcher.find_application(app)
        print(f"  Found {len(apps)} applications for '{app}'")
        for app_info in apps[:2]:  # Show first 2
            print(f"    - {app_info.name} at {app_info.path}")
    
    print("\n" + "=" * 60)


def demo_nlp_pipeline():
    """Demonstrate NLP Pipeline."""
    print("DEMO: Natural Language Processing Pipeline")
    print("=" * 60)
    
    from nlp.intent_classifier import HybridIntentClassifier, IntentType
    from nlp.text_processor import TextProcessor
    
    # Test intent classification
    print("Testing Intent Classification:")
    classifier = HybridIntentClassifier()
    
    # Add training data
    training_examples = [
        ("hello there", IntentType.GREETING),
        ("what time is it", IntentType.TIME_QUERY),
        ("set a reminder for 3pm", IntentType.REMINDER_SET),
        ("open calculator", IntentType.APP_LAUNCH),
        ("what's the weather like", IntentType.WEATHER_QUERY),
    ]
    
    for text, intent in training_examples:
        classifier.add_training_data(text, intent)
    
    classifier.train_ml()
    
    # Test classification
    test_phrases = [
        "Hey there, how are you?",
        "What time is it right now?",
        "Remind me to call mom at 5pm",
        "Open the calculator app",
        "What's the weather forecast?"
    ]
    
    for phrase in test_phrases:
        result = classifier.classify(phrase)
        print(f"  '{phrase}' -> {result.intent.value} (confidence: {result.confidence:.2f})")
    
    # Test text processing
    print("\nTesting Text Processing:")
    processor = TextProcessor()
    
    test_text = "Hello! I'm excited to tell you about our amazing new product. It's absolutely fantastic!"
    
    processed = processor.process(test_text)
    print(f"  Original: {test_text}")
    print(f"  Cleaned: {processed.cleaned_text}")
    print(f"  Tokens: {processed.tokens[:5]}...")  # First 5 tokens
    print(f"  Sentiment: {processed.sentiment_score:.2f}")
    print(f"  Key phrases: {processed.key_phrases[:3]}")  # First 3 key phrases
    
    # Test entity extraction
    entities = processor.extract_entities(test_text)
    print(f"  Entities: {entities}")
    
    print("\n" + "=" * 60)


def demo_skills_framework():
    """Demonstrate Skills Framework."""
    print("DEMO: Extensible Skills Framework")
    print("=" * 60)
    
    from skills.base_skill import SkillManager, SkillContext
    from skills.reminder_skill import ReminderSkill
    from core.scheduler import PriorityScheduler
    
    # Create skill manager
    manager = SkillManager()
    scheduler = PriorityScheduler()
    
    # Register reminder skill
    reminder_skill = ReminderSkill(scheduler)
    manager.register_skill(reminder_skill)
    
    print(f"Registered {len(manager.skills)} skills")
    
    # Test skill execution
    print("\nTesting skill execution:")
    test_contexts = [
        SkillContext(
            user_input="Remind me to call mom at 3pm",
            intent="reminder_set",
            entities={},
            confidence=0.9,
            session_id="test"
        ),
        SkillContext(
            user_input="What reminders do I have?",
            intent="reminder_query",
            entities={},
            confidence=0.9,
            session_id="test"
        )
    ]
    
    for context in test_contexts:
        result = manager.execute_best_skill(context)
        print(f"  Input: {context.user_input}")
        print(f"  Result: {result.message}")
        print(f"  Success: {result.success}")
        print()
    
    # Show skill statistics
    stats = manager.get_skill_statistics()
    print(f"Skill statistics: {stats}")
    
    scheduler.shutdown()
    
    print("\n" + "=" * 60)


def main():
    """Run all demos."""
    print("SIGMA VOICE ASSISTANT - ALGORITHM DEMONSTRATIONS")
    print("=" * 60)
    print("This demo showcases the advanced data structures and algorithms")
    print("used in the Sigma Voice Assistant project.")
    print("=" * 60)
    
    try:
        demo_trie_algorithm()
        demo_state_machine()
        demo_scheduler()
        demo_cache()
        demo_graph_search()
        demo_nlp_pipeline()
        demo_skills_framework()
        
        print("\n" + "=" * 60)
        print("ALL DEMOS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("The Sigma Voice Assistant demonstrates:")
        print("[OK] Trie-based keyword matching for fast text search")
        print("[OK] Finite state machine for dialogue management")
        print("[OK] Priority heap-based task scheduling")
        print("[OK] LRU cache for performance optimization")
        print("[OK] Graph-based search algorithms")
        print("[OK] Machine learning for intent classification")
        print("[OK] Extensible plugin architecture")
        print("[OK] Modern software engineering practices")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nDemo error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
