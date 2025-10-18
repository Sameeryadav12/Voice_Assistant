"""
LRU Cache implementation with advanced features for voice assistant data management.
Demonstrates cache algorithms, memory management, and performance optimization.
"""

from typing import Any, Optional, Dict, List, Tuple, Callable
from collections import OrderedDict, defaultdict
import threading
import time
import hashlib
import json
from dataclasses import dataclass
from enum import Enum


class CachePolicy(Enum):
    """Cache eviction policies."""
    LRU = "lru"  # Least Recently Used
    LFU = "lfu"  # Least Frequently Used
    TTL = "ttl"  # Time To Live
    SIZE = "size"  # Size-based eviction


@dataclass
class CacheEntry:
    """Represents a cache entry with metadata."""
    key: str
    value: Any
    created_at: float
    last_accessed: float
    access_count: int = 0
    size_bytes: int = 0
    ttl: Optional[float] = None
    priority: int = 0
    
    def is_expired(self) -> bool:
        """Check if the entry has expired."""
        if self.ttl is None:
            return False
        return time.time() - self.created_at > self.ttl
    
    def update_access(self) -> None:
        """Update access statistics."""
        self.last_accessed = time.time()
        self.access_count += 1


class AdvancedLRUCache:
    """
    Advanced LRU Cache with multiple eviction policies and performance optimizations.
    Features:
    - Multiple eviction policies (LRU, LFU, TTL, Size-based)
    - Thread-safe operations
    - Memory usage tracking
    - Hit/miss ratio monitoring
    - Automatic cleanup
    - Cache warming
    - Compression support
    """
    
    def __init__(self, 
                 max_size: int = 1000,
                 max_memory_mb: float = 100.0,
                 policy: CachePolicy = CachePolicy.LRU,
                 default_ttl: Optional[float] = None,
                 compression_threshold: int = 1024):
        self.max_size = max_size
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.policy = policy
        self.default_ttl = default_ttl
        self.compression_threshold = compression_threshold
        
        # Core cache storage
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self.lock = threading.RLock()
        
        # Statistics
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.current_memory_usage = 0
        
        # Frequency tracking for LFU policy
        self.frequency_map: Dict[str, int] = defaultdict(int)
        
        # Cleanup thread
        self.cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self.cleanup_thread.start()
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache."""
        with self.lock:
            if key not in self.cache:
                self.misses += 1
                return None
            
            entry = self.cache[key]
            
            # Check if expired
            if entry.is_expired():
                self._remove_entry(key)
                self.misses += 1
                return None
            
            # Update access statistics
            entry.update_access()
            self.frequency_map[key] += 1
            
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            
            self.hits += 1
            return entry.value
    
    def put(self, key: str, value: Any, ttl: Optional[float] = None, 
            priority: int = 0) -> None:
        """Put a value into the cache."""
        with self.lock:
            # Calculate size
            size_bytes = self._calculate_size(value)
            
            # Use default TTL if not specified
            if ttl is None:
                ttl = self.default_ttl
            
            # Create entry
            entry = CacheEntry(
                key=key,
                value=value,
                created_at=time.time(),
                last_accessed=time.time(),
                size_bytes=size_bytes,
                ttl=ttl,
                priority=priority
            )
            
            # Remove existing entry if present
            if key in self.cache:
                self._remove_entry(key)
            
            # Check if we need to evict
            while (len(self.cache) >= self.max_size or 
                   self.current_memory_usage + size_bytes > self.max_memory_bytes):
                self._evict_entry()
            
            # Add new entry
            self.cache[key] = entry
            self.current_memory_usage += size_bytes
            self.frequency_map[key] = 1
    
    def delete(self, key: str) -> bool:
        """Delete a key from the cache."""
        with self.lock:
            if key in self.cache:
                self._remove_entry(key)
                return True
            return False
    
    def clear(self) -> None:
        """Clear all entries from the cache."""
        with self.lock:
            self.cache.clear()
            self.frequency_map.clear()
            self.current_memory_usage = 0
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self.lock:
            total_requests = self.hits + self.misses
            hit_ratio = (self.hits / total_requests * 100) if total_requests > 0 else 0
            
            return {
                'size': len(self.cache),
                'max_size': self.max_size,
                'memory_usage_mb': self.current_memory_usage / (1024 * 1024),
                'max_memory_mb': self.max_memory_bytes / (1024 * 1024),
                'hits': self.hits,
                'misses': self.misses,
                'hit_ratio': hit_ratio,
                'evictions': self.evictions,
                'policy': self.policy.value
            }
    
    def get_top_keys(self, limit: int = 10) -> List[Tuple[str, int]]:
        """Get most frequently accessed keys."""
        with self.lock:
            return sorted(self.frequency_map.items(), key=lambda x: x[1], reverse=True)[:limit]
    
    def warm_cache(self, key_value_pairs: List[Tuple[str, Any]]) -> None:
        """Warm the cache with initial data."""
        for key, value in key_value_pairs:
            self.put(key, value)
    
    def _remove_entry(self, key: str) -> None:
        """Remove an entry from the cache."""
        if key in self.cache:
            entry = self.cache[key]
            self.current_memory_usage -= entry.size_bytes
            del self.cache[key]
            if key in self.frequency_map:
                del self.frequency_map[key]
    
    def _evict_entry(self) -> None:
        """Evict an entry based on the current policy."""
        if not self.cache:
            return
        
        if self.policy == CachePolicy.LRU:
            # Remove least recently used (first item)
            key_to_remove = next(iter(self.cache))
        elif self.policy == CachePolicy.LFU:
            # Remove least frequently used
            key_to_remove = min(self.frequency_map.items(), key=lambda x: x[1])[0]
        elif self.policy == CachePolicy.TTL:
            # Remove oldest entry
            key_to_remove = min(self.cache.items(), key=lambda x: x[1].created_at)[0]
        elif self.policy == CachePolicy.SIZE:
            # Remove largest entry
            key_to_remove = max(self.cache.items(), key=lambda x: x[1].size_bytes)[0]
        else:
            # Default to LRU
            key_to_remove = next(iter(self.cache))
        
        self._remove_entry(key_to_remove)
        self.evictions += 1
    
    def _calculate_size(self, value: Any) -> int:
        """Calculate the size of a value in bytes."""
        try:
            if isinstance(value, str):
                return len(value.encode('utf-8'))
            elif isinstance(value, (int, float)):
                return 8
            elif isinstance(value, dict):
                return len(json.dumps(value, default=str).encode('utf-8'))
            elif isinstance(value, list):
                return sum(self._calculate_size(item) for item in value)
            else:
                return len(str(value).encode('utf-8'))
        except:
            return 1024  # Default size for unknown types
    
    def _cleanup_loop(self) -> None:
        """Background cleanup loop for expired entries."""
        while True:
            try:
                time.sleep(60)  # Cleanup every minute
                self._cleanup_expired()
            except Exception as e:
                print(f"Cache cleanup error: {e}")
    
    def _cleanup_expired(self) -> None:
        """Remove expired entries."""
        with self.lock:
            expired_keys = []
            for key, entry in self.cache.items():
                if entry.is_expired():
                    expired_keys.append(key)
            
            for key in expired_keys:
                self._remove_entry(key)


class CacheManager:
    """
    High-level cache manager for the voice assistant.
    Manages multiple caches for different types of data.
    """
    
    def __init__(self):
        self.caches: Dict[str, AdvancedLRUCache] = {}
        self._setup_caches()
    
    def _setup_caches(self) -> None:
        """Setup different caches for different data types."""
        # Speech recognition cache
        self.caches['speech'] = AdvancedLRUCache(
            max_size=1000,
            max_memory_mb=50,
            policy=CachePolicy.LRU,
            default_ttl=3600  # 1 hour
        )
        
        # Intent classification cache
        self.caches['intent'] = AdvancedLRUCache(
            max_size=500,
            max_memory_mb=25,
            policy=CachePolicy.LFU,
            default_ttl=7200  # 2 hours
        )
        
        # Response cache
        self.caches['response'] = AdvancedLRUCache(
            max_size=200,
            max_memory_mb=30,
            policy=CachePolicy.TTL,
            default_ttl=1800  # 30 minutes
        )
        
        # File system cache
        self.caches['filesystem'] = AdvancedLRUCache(
            max_size=2000,
            max_memory_mb=100,
            policy=CachePolicy.SIZE,
            default_ttl=3600
        )
    
    def get_cache(self, cache_type: str) -> Optional[AdvancedLRUCache]:
        """Get a specific cache by type."""
        return self.caches.get(cache_type)
    
    def cache_speech_result(self, audio_hash: str, text: str, confidence: float) -> None:
        """Cache speech recognition result."""
        cache = self.caches['speech']
        cache.put(audio_hash, {
            'text': text,
            'confidence': confidence,
            'timestamp': time.time()
        })
    
    def get_speech_result(self, audio_hash: str) -> Optional[Dict]:
        """Get cached speech recognition result."""
        cache = self.caches['speech']
        return cache.get(audio_hash)
    
    def cache_intent_result(self, text: str, intent: str, confidence: float) -> None:
        """Cache intent classification result."""
        cache = self.caches['intent']
        text_hash = hashlib.md5(text.encode()).hexdigest()
        cache.put(text_hash, {
            'intent': intent,
            'confidence': confidence,
            'timestamp': time.time()
        })
    
    def get_intent_result(self, text: str) -> Optional[Dict]:
        """Get cached intent classification result."""
        cache = self.caches['intent']
        text_hash = hashlib.md5(text.encode()).hexdigest()
        return cache.get(text_hash)
    
    def cache_response(self, query: str, response: str) -> None:
        """Cache generated response."""
        cache = self.caches['response']
        query_hash = hashlib.md5(query.encode()).hexdigest()
        cache.put(query_hash, {
            'response': response,
            'timestamp': time.time()
        })
    
    def get_response(self, query: str) -> Optional[Dict]:
        """Get cached response."""
        cache = self.caches['response']
        query_hash = hashlib.md5(query.encode()).hexdigest()
        return cache.get(query_hash)
    
    def get_all_statistics(self) -> Dict[str, Dict]:
        """Get statistics for all caches."""
        return {name: cache.get_statistics() for name, cache in self.caches.items()}
    
    def clear_all_caches(self) -> None:
        """Clear all caches."""
        for cache in self.caches.values():
            cache.clear()


if __name__ == "__main__":
    # Demo the cache system
    cache_manager = CacheManager()
    
    # Test speech recognition caching
    audio_hash = "test_audio_123"
    cache_manager.cache_speech_result(audio_hash, "Hello world", 0.95)
    
    result = cache_manager.get_speech_result(audio_hash)
    print("Cached speech result:", result)
    
    # Test intent caching
    cache_manager.cache_intent_result("What time is it?", "time_query", 0.9)
    intent_result = cache_manager.get_intent_result("What time is it?")
    print("Cached intent result:", intent_result)
    
    # Test response caching
    cache_manager.cache_response("What time is it?", "It's 3:30 PM")
    response = cache_manager.get_response("What time is it?")
    print("Cached response:", response)
    
    # Show statistics
    print("\nCache statistics:")
    for name, stats in cache_manager.get_all_statistics().items():
        print(f"{name}: {stats}")






