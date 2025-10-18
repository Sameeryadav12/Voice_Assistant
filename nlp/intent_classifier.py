"""
Intent classification system using pattern matching and machine learning approaches.
Demonstrates NLP algorithms, text processing, and classification techniques.
"""

import re
import json
import time
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict, Counter
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import threading


class IntentType(Enum):
    """Types of user intents."""
    GREETING = "greeting"
    TIME_QUERY = "time_query"
    WEATHER_QUERY = "weather_query"
    REMINDER_SET = "reminder_set"
    REMINDER_QUERY = "reminder_query"
    FILE_SEARCH = "file_search"
    APP_LAUNCH = "app_launch"
    CALCULATION = "calculation"
    SEARCH_WEB = "search_web"
    MUSIC_CONTROL = "music_control"
    SYSTEM_CONTROL = "system_control"
    UNKNOWN = "unknown"


@dataclass
class IntentResult:
    """Result of intent classification."""
    intent: IntentType
    confidence: float
    entities: Dict[str, Any]
    raw_text: str
    processing_time: float


class PatternMatcher:
    """
    Pattern-based intent classification using regex and keyword matching.
    Demonstrates rule-based NLP and pattern recognition algorithms.
    """
    
    def __init__(self):
        self.patterns = self._build_patterns()
        self.keyword_weights = self._build_keyword_weights()
    
    def _build_patterns(self) -> Dict[IntentType, List[str]]:
        """Build regex patterns for intent classification."""
        return {
            IntentType.GREETING: [
                r'\b(hello|hi|hey|good morning|good afternoon|good evening)\b',
                r'\b(how are you|what\'s up|how do you do)\b'
            ],
            IntentType.TIME_QUERY: [
                r'\b(what time|current time|time now|clock)\b',
                r'\b(what\'s the time|tell me the time)\b'
            ],
            IntentType.WEATHER_QUERY: [
                r'\b(weather|temperature|forecast|rain|sunny|cloudy)\b',
                r'\b(what\'s the weather|how\'s the weather)\b'
            ],
            IntentType.REMINDER_SET: [
                r'\b(remind me|set reminder|create reminder|schedule)\b',
                r'\b(remind me to|don\'t forget|remember to)\b'
            ],
            IntentType.REMINDER_QUERY: [
                r'\b(what reminders|my reminders|reminder list)\b',
                r'\b(do i have|any reminders)\b'
            ],
            IntentType.FILE_SEARCH: [
                r'\b(find file|search for|look for|file named)\b',
                r'\b(where is|locate|open file)\b'
            ],
            IntentType.APP_LAUNCH: [
                r'\b(open|launch|start|run)\b.*\b(app|application|program)\b',
                r'\b(open|launch|start)\b.*\b(calculator|notepad|browser|terminal)\b'
            ],
            IntentType.CALCULATION: [
                r'\b(calculate|compute|what is|how much)\b.*\b(\d+|\+|\-|\*|\/)\b',
                r'\b(math|arithmetic|add|subtract|multiply|divide)\b'
            ],
            IntentType.SEARCH_WEB: [
                r'\b(search for|look up|google|find information)\b',
                r'\b(what is|who is|when is|where is)\b'
            ],
            IntentType.MUSIC_CONTROL: [
                r'\b(play|pause|stop|next|previous)\b.*\b(music|song|track)\b',
                r'\b(volume|louder|quieter|mute)\b'
            ],
            IntentType.SYSTEM_CONTROL: [
                r'\b(shutdown|restart|sleep|lock|logout)\b',
                r'\b(close|minimize|maximize)\b.*\b(window|app|program)\b'
            ]
        }
    
    def _build_keyword_weights(self) -> Dict[str, Dict[IntentType, float]]:
        """Build keyword weights for intent classification."""
        return {
            'time': {IntentType.TIME_QUERY: 0.9, IntentType.REMINDER_SET: 0.3},
            'weather': {IntentType.WEATHER_QUERY: 0.9},
            'remind': {IntentType.REMINDER_SET: 0.8, IntentType.REMINDER_QUERY: 0.6},
            'file': {IntentType.FILE_SEARCH: 0.8},
            'open': {IntentType.APP_LAUNCH: 0.7, IntentType.FILE_SEARCH: 0.4},
            'calculate': {IntentType.CALCULATION: 0.9},
            'search': {IntentType.SEARCH_WEB: 0.8, IntentType.FILE_SEARCH: 0.5},
            'play': {IntentType.MUSIC_CONTROL: 0.8},
            'hello': {IntentType.GREETING: 0.9},
            'shutdown': {IntentType.SYSTEM_CONTROL: 0.9}
        }
    
    def classify(self, text: str) -> Tuple[IntentType, float, Dict[str, Any]]:
        """Classify intent using pattern matching."""
        text_lower = text.lower()
        intent_scores = defaultdict(float)
        matched_patterns = []
        entities = {}
        
        # Pattern matching
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                if matches:
                    intent_scores[intent] += len(matches) * 0.3
                    matched_patterns.append((intent, pattern, matches))
        
        # Keyword weighting
        words = text_lower.split()
        for word in words:
            if word in self.keyword_weights:
                for intent, weight in self.keyword_weights[word].items():
                    intent_scores[intent] += weight
        
        # Extract entities
        entities = self._extract_entities(text)
        
        # Determine best intent
        if intent_scores:
            best_intent = max(intent_scores.items(), key=lambda x: x[1])
            confidence = min(best_intent[1], 1.0)
            return best_intent[0], confidence, entities
        else:
            return IntentType.UNKNOWN, 0.0, entities
    
    def _extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract entities from text."""
        entities = {}
        
        # Time entities
        time_patterns = [
            r'\b(\d{1,2}):(\d{2})\s*(am|pm)?\b',
            r'\b(\d{1,2})\s*(am|pm)\b',
            r'\b(morning|afternoon|evening|night)\b'
        ]
        
        for pattern in time_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                entities['time'] = matches[0]
                break
        
        # Duration entities
        duration_patterns = [
            r'\b(\d+)\s*(minute|hour|day|week|month|year)s?\b',
            r'\b(in|after)\s+(\d+)\s*(minute|hour|day|week|month|year)s?\b'
        ]
        
        for pattern in duration_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                entities['duration'] = matches[0]
                break
        
        # File/App names
        app_patterns = [
            r'\b(open|launch|start)\s+([a-zA-Z0-9\s]+?)(?:\s|$)',
            r'\b(find|search for)\s+([a-zA-Z0-9\s]+?)(?:\s|$)'
        ]
        
        for pattern in app_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                entities['target'] = matches[0][1].strip()
                break
        
        return entities


class MLIntentClassifier:
    """
    Machine learning-based intent classification.
    Demonstrates ML algorithms for text classification.
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.classifier = None
        self.intent_labels = []
        self.training_data = []
        self.is_trained = False
        self.lock = threading.Lock()
    
    def add_training_data(self, text: str, intent: IntentType) -> None:
        """Add training data for the classifier."""
        with self.lock:
            self.training_data.append((text, intent))
    
    def train(self) -> bool:
        """Train the ML classifier."""
        if len(self.training_data) < 10:
            return False
        
        try:
            with self.lock:
                texts, labels = zip(*self.training_data)
                
                # Vectorize texts
                X = self.vectorizer.fit_transform(texts)
                
                # Get unique labels
                self.intent_labels = list(set(labels))
                label_to_idx = {label: idx for idx, label in enumerate(self.intent_labels)}
                y = [label_to_idx[label] for label in labels]
                
                # Train classifier
                self.classifier = RandomForestClassifier(n_estimators=100, random_state=42)
                self.classifier.fit(X, y)
                
                self.is_trained = True
                return True
                
        except Exception as e:
            print(f"Error training ML classifier: {e}")
            return False
    
    def classify(self, text: str) -> Tuple[IntentType, float, Dict[str, Any]]:
        """Classify intent using ML model."""
        if not self.is_trained:
            return IntentType.UNKNOWN, 0.0, {}
        
        try:
            with self.lock:
                # Vectorize text
                X = self.vectorizer.transform([text])
                
                # Predict
                prediction = self.classifier.predict(X)[0]
                probabilities = self.classifier.predict_proba(X)[0]
                
                # Get confidence
                confidence = max(probabilities)
                
                # Get intent
                intent = self.intent_labels[prediction]
                
                return intent, confidence, {}
                
        except Exception as e:
            print(f"Error in ML classification: {e}")
            return IntentType.UNKNOWN, 0.0, {}
    
    def get_training_stats(self) -> Dict[str, Any]:
        """Get training statistics."""
        with self.lock:
            if not self.training_data:
                return {'total_samples': 0, 'intent_distribution': {}}
            
            texts, labels = zip(*self.training_data)
            intent_counts = Counter(labels)
            
            return {
                'total_samples': len(self.training_data),
                'intent_distribution': dict(intent_counts),
                'is_trained': self.is_trained
            }


class HybridIntentClassifier:
    """
    Hybrid intent classifier combining pattern matching and ML approaches.
    Demonstrates ensemble methods and confidence-based decision making.
    """
    
    def __init__(self):
        self.pattern_matcher = PatternMatcher()
        self.ml_classifier = MLIntentClassifier()
        self.confidence_threshold = 0.7
        self.fallback_to_pattern = True
    
    def add_training_data(self, text: str, intent: IntentType) -> None:
        """Add training data for ML component."""
        self.ml_classifier.add_training_data(text, intent)
    
    def train_ml(self) -> bool:
        """Train the ML component."""
        return self.ml_classifier.train()
    
    def classify(self, text: str) -> IntentResult:
        """Classify intent using hybrid approach."""
        start_time = time.time()
        
        # Get pattern-based classification
        pattern_intent, pattern_confidence, pattern_entities = self.pattern_matcher.classify(text)
        
        # Get ML-based classification
        ml_intent, ml_confidence, ml_entities = self.ml_classifier.classify(text)
        
        # Combine results
        final_intent, final_confidence, final_entities = self._combine_results(
            pattern_intent, pattern_confidence, pattern_entities,
            ml_intent, ml_confidence, ml_entities
        )
        
        processing_time = time.time() - start_time
        
        return IntentResult(
            intent=final_intent,
            confidence=final_confidence,
            entities=final_entities,
            raw_text=text,
            processing_time=processing_time
        )
    
    def _combine_results(self, 
                        pattern_intent: IntentType, pattern_confidence: float, pattern_entities: Dict,
                        ml_intent: IntentType, ml_confidence: float, ml_entities: Dict) -> Tuple[IntentType, float, Dict]:
        """Combine pattern and ML results."""
        
        # If ML is not trained, use pattern matching
        if not self.ml_classifier.is_trained:
            return pattern_intent, pattern_confidence, pattern_entities
        
        # If both agree, use higher confidence
        if pattern_intent == ml_intent:
            confidence = max(pattern_confidence, ml_confidence)
            entities = {**pattern_entities, **ml_entities}
            return pattern_intent, confidence, entities
        
        # If ML confidence is high, prefer ML
        if ml_confidence > self.confidence_threshold:
            return ml_intent, ml_confidence, ml_entities
        
        # If pattern confidence is high, prefer pattern
        if pattern_confidence > self.confidence_threshold:
            return pattern_intent, pattern_confidence, pattern_entities
        
        # If both are low confidence, use pattern as fallback
        if self.fallback_to_pattern:
            return pattern_intent, pattern_confidence, pattern_entities
        else:
            return IntentType.UNKNOWN, 0.0, {}
    
    def get_classification_stats(self) -> Dict[str, Any]:
        """Get classification statistics."""
        return {
            'ml_stats': self.ml_classifier.get_training_stats(),
            'confidence_threshold': self.confidence_threshold,
            'fallback_to_pattern': self.fallback_to_pattern
        }


if __name__ == "__main__":
    # Demo the intent classifier
    classifier = HybridIntentClassifier()
    
    # Add some training data
    training_examples = [
        ("hello there", IntentType.GREETING),
        ("what time is it", IntentType.TIME_QUERY),
        ("set a reminder for 3pm", IntentType.REMINDER_SET),
        ("open calculator", IntentType.APP_LAUNCH),
        ("what's the weather like", IntentType.WEATHER_QUERY),
        ("find my documents", IntentType.FILE_SEARCH),
        ("calculate 2 plus 2", IntentType.CALCULATION),
        ("play some music", IntentType.MUSIC_CONTROL),
        ("search for python tutorials", IntentType.SEARCH_WEB)
    ]
    
    for text, intent in training_examples:
        classifier.add_training_data(text, intent)
    
    # Train the ML component
    print("Training ML classifier...")
    classifier.train_ml()
    
    # Test classification
    test_phrases = [
        "Hey there, how are you?",
        "What time is it right now?",
        "Remind me to call mom at 5pm",
        "Open the calculator app",
        "What's the weather forecast?",
        "Find files containing 'project'",
        "What is 15 times 7?",
        "Play my favorite song",
        "Search for machine learning courses"
    ]
    
    print("\nTesting intent classification:")
    for phrase in test_phrases:
        result = classifier.classify(phrase)
        print(f"'{phrase}' -> {result.intent.value} (confidence: {result.confidence:.2f})")
        if result.entities:
            print(f"  Entities: {result.entities}")
    
    # Show statistics
    print(f"\nClassification stats: {classifier.get_classification_stats()}")




