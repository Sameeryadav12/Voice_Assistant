"""
Trie-based keyword matching system for efficient wake word detection and command recognition.
Demonstrates advanced string matching algorithms and memory optimization.
"""

from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict
import time


class TrieNode:
    """Node in the trie data structure with optimized memory usage."""
    
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word: bool = False
        self.frequency: int = 0
        self.metadata: Dict = {}
        self.failure_link: Optional['TrieNode'] = None  # For Aho-Corasick algorithm


class AdvancedTrie:
    """
    Advanced Trie implementation with multiple search algorithms:
    - Exact matching
    - Fuzzy matching with Levenshtein distance
    - Aho-Corasick for multiple pattern matching
    - Frequency-based ranking
    """
    
    def __init__(self):
        self.root = TrieNode()
        self.size = 0
        self.max_fuzzy_distance = 2
        
    def insert(self, word: str, metadata: Dict = None, frequency: int = 1) -> None:
        """Insert a word into the trie with O(m) complexity where m is word length."""
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        if not node.is_end_of_word:
            self.size += 1
            node.is_end_of_word = True
        
        node.frequency += frequency
        if metadata:
            node.metadata.update(metadata)
    
    def search_exact(self, word: str) -> bool:
        """Exact search with O(m) complexity."""
        node = self._get_node(word)
        return node is not None and node.is_end_of_word
    
    def search_fuzzy(self, word: str, max_distance: int = None) -> List[Tuple[str, int, Dict]]:
        """
        Fuzzy search using dynamic programming for Levenshtein distance.
        Time complexity: O(n * m * d) where n=words, m=length, d=distance
        """
        if max_distance is None:
            max_distance = self.max_fuzzy_distance
        
        results = []
        self._fuzzy_search_recursive(
            self.root, word.lower(), "", max_distance, results
        )
        
        # Sort by distance, then by frequency
        return sorted(results, key=lambda x: (x[1], -x[2].get('frequency', 0)))
    
    def search_prefix(self, prefix: str) -> List[str]:
        """Find all words with given prefix using BFS."""
        node = self._get_node(prefix)
        if not node:
            return []
        
        results = []
        self._collect_words(node, prefix, results)
        return results
    
    def aho_corasick_search(self, text: str) -> List[Tuple[str, int, Dict]]:
        """
        Aho-Corasick algorithm for multiple pattern matching.
        Time complexity: O(n + m + z) where n=text length, m=total pattern length, z=matches
        """
        self._build_failure_links()
        results = []
        current = self.root
        
        for i, char in enumerate(text.lower()):
            # Follow failure links if character not found
            while current != self.root and char not in current.children:
                current = current.failure_link
            
            if char in current.children:
                current = current.children[char]
            
            # Check for matches at current position
            temp = current
            while temp != self.root:
                if temp.is_end_of_word:
                    results.append((text[i-len(self._get_word_from_node(temp))+1:i+1], i, temp.metadata))
                temp = temp.failure_link
        
        return results
    
    def get_top_k_frequent(self, k: int = 10) -> List[Tuple[str, int]]:
        """Get top k most frequent words using heap-based selection."""
        import heapq
        
        heap = []
        self._collect_frequencies(self.root, "", heap)
        
        # Use heap to get top k elements
        return heapq.nlargest(k, heap, key=lambda x: x[1])
    
    def _get_node(self, word: str) -> Optional[TrieNode]:
        """Helper method to get node for a word."""
        node = self.root
        for char in word.lower():
            if char not in node.children:
                return None
            node = node.children[char]
        return node
    
    def _fuzzy_search_recursive(self, node: TrieNode, word: str, current: str, 
                               max_distance: int, results: List) -> None:
        """Recursive fuzzy search with dynamic programming optimization."""
        if not word and node.is_end_of_word:
            results.append((current, 0, node.metadata))
            return
        
        if not word:
            return
        
        # Exact match
        if word[0] in node.children:
            self._fuzzy_search_recursive(
                node.children[word[0]], word[1:], current + word[0], 
                max_distance, results
            )
        
        # Insertion, deletion, substitution
        if max_distance > 0:
            for char, child in node.children.items():
                # Substitution
                self._fuzzy_search_recursive(
                    child, word[1:], current + char, 
                    max_distance - 1, results
                )
                # Insertion
                self._fuzzy_search_recursive(
                    child, word, current + char, 
                    max_distance - 1, results
                )
            
            # Deletion
            self._fuzzy_search_recursive(
                node, word[1:], current, 
                max_distance - 1, results
            )
    
    def _collect_words(self, node: TrieNode, prefix: str, results: List[str]) -> None:
        """Collect all words from a node using DFS."""
        if node.is_end_of_word:
            results.append(prefix)
        
        for char, child in node.children.items():
            self._collect_words(child, prefix + char, results)
    
    def _collect_frequencies(self, node: TrieNode, current: str, heap: List) -> None:
        """Collect word frequencies for heap operations."""
        if node.is_end_of_word:
            heap.append((current, node.frequency))
        
        for char, child in node.children.items():
            self._collect_frequencies(child, current + char, heap)
    
    def _build_failure_links(self) -> None:
        """Build failure links for Aho-Corasick algorithm using BFS."""
        from collections import deque
        
        queue = deque()
        self.root.failure_link = self.root
        
        # Initialize queue with root's children
        for child in self.root.children.values():
            child.failure_link = self.root
            queue.append(child)
        
        while queue:
            current = queue.popleft()
            
            for char, child in current.children.items():
                queue.append(child)
                
                # Find failure link for child
                failure = current.failure_link
                while failure != self.root and char not in failure.children:
                    failure = failure.failure_link
                
                if char in failure.children:
                    child.failure_link = failure.children[char]
                else:
                    child.failure_link = self.root
    
    def _get_word_from_node(self, node: TrieNode) -> str:
        """Helper to reconstruct word from node (simplified for demo)."""
        # In a full implementation, you'd store the word path
        return ""


class KeywordMatcher:
    """
    High-level keyword matching system using the advanced trie.
    Provides intelligent wake word detection and command recognition.
    """
    
    def __init__(self):
        self.trie = AdvancedTrie()
        # Add phonetic variations to handle accents and mishearing
        self.wake_words = {
            "hey sigma", "sigma", "assistant",
            "play sigma", "hey cig", "cig", "say sigma",  # Common mishearings
            "hey cigma", "cigma", "hey sig", "sig",
            "a sigma", "hey signal", "signal",
            "hey seema", "seema", "hey sigma"
        }
        self.command_keywords = {
            "reminder": ["remind", "reminder", "schedule", "alarm"],
            "file": ["file", "search", "find", "open"],
            "app": ["open", "launch", "start", "run"],
            "weather": ["weather", "temperature", "forecast"],
            "time": ["time", "clock", "date"]
        }
        self._initialize_keywords()
    
    def _initialize_keywords(self) -> None:
        """Initialize the trie with wake words and command keywords."""
        # Add wake words
        for wake_word in self.wake_words:
            self.trie.insert(wake_word, {"type": "wake_word", "priority": 1})
        
        # Add command keywords
        for intent, keywords in self.command_keywords.items():
            for keyword in keywords:
                self.trie.insert(
                    keyword, 
                    {"type": "command", "intent": intent, "priority": 2}
                )
    
    def detect_wake_word(self, text: str) -> bool:
        """Detect if wake word is present in text."""
        matches = self.trie.aho_corasick_search(text)
        return any(match[2].get("type") == "wake_word" for match in matches)
    
    def extract_intent(self, text: str) -> Optional[str]:
        """Extract user intent from text using fuzzy matching."""
        # Remove wake word if present
        clean_text = text.lower()
        for wake_word in self.wake_words:
            clean_text = clean_text.replace(wake_word, "").strip()
        
        # Find best matching intent
        matches = self.trie.aho_corasick_search(clean_text)
        if not matches:
            return None
        
        # Return most frequent intent
        intent_counts = defaultdict(int)
        for _, _, metadata in matches:
            if metadata.get("type") == "command":
                intent_counts[metadata.get("intent")] += 1
        
        return max(intent_counts.items(), key=lambda x: x[1])[0] if intent_counts else None
    
    def get_suggestions(self, partial_text: str, limit: int = 5) -> List[str]:
        """Get command suggestions based on partial input."""
        suggestions = self.trie.search_prefix(partial_text.lower())
        return suggestions[:limit]


# Performance testing and benchmarking
class TrieBenchmark:
    """Benchmarking utilities for trie performance analysis."""
    
    @staticmethod
    def benchmark_insertion(trie: AdvancedTrie, words: List[str]) -> float:
        """Benchmark insertion performance."""
        start_time = time.time()
        for word in words:
            trie.insert(word)
        return time.time() - start_time
    
    @staticmethod
    def benchmark_search(trie: AdvancedTrie, words: List[str]) -> float:
        """Benchmark search performance."""
        start_time = time.time()
        for word in words:
            trie.search_exact(word)
        return time.time() - start_time
    
    @staticmethod
    def benchmark_fuzzy_search(trie: AdvancedTrie, words: List[str]) -> float:
        """Benchmark fuzzy search performance."""
        start_time = time.time()
        for word in words:
            trie.search_fuzzy(word)
        return time.time() - start_time


if __name__ == "__main__":
    # Demo and testing
    trie = AdvancedTrie()
    matcher = KeywordMatcher()
    
    # Test basic functionality
    test_words = ["hello", "world", "python", "algorithm", "data", "structure"]
    for word in test_words:
        trie.insert(word)
    
    print("Trie size:", trie.size)
    print("Search 'hello':", trie.search_exact("hello"))
    print("Search 'hell':", trie.search_exact("hell"))
    print("Fuzzy search 'helo':", trie.search_fuzzy("helo"))
    print("Prefix search 'he':", trie.search_prefix("he"))
    
    # Test keyword matcher
    print("\nWake word detection:")
    print("'Hey Sigma, what time is it?' ->", matcher.detect_wake_word("Hey Sigma, what time is it?"))
    print("'Hello world' ->", matcher.detect_wake_word("Hello world"))
    
    print("\nIntent extraction:")
    print("'Hey Sigma, set a reminder' ->", matcher.extract_intent("Hey Sigma, set a reminder"))
    print("'Open calculator' ->", matcher.extract_intent("Open calculator"))






