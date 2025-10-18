"""
Text processing utilities for natural language understanding.
Demonstrates text preprocessing, normalization, and feature extraction algorithms.
"""

import re
import string
import unicodedata
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass
from collections import Counter, defaultdict
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
import threading


@dataclass
class ProcessedText:
    """Result of text processing."""
    original_text: str
    cleaned_text: str
    tokens: List[str]
    lemmatized_tokens: List[str]
    pos_tags: List[Tuple[str, str]]
    named_entities: List[Tuple[str, str]]
    sentiment_score: float
    key_phrases: List[str]
    word_frequencies: Dict[str, int]


class TextNormalizer:
    """
    Text normalization and cleaning utilities.
    Demonstrates text preprocessing algorithms and Unicode handling.
    """
    
    def __init__(self):
        self.contractions = {
            "don't": "do not", "won't": "will not", "can't": "cannot",
            "n't": " not", "'re": " are", "'s": " is", "'d": " would",
            "'ll": " will", "'ve": " have", "'m": " am"
        }
        self.punctuation_table = str.maketrans('', '', string.punctuation)
    
    def normalize(self, text: str) -> str:
        """Normalize text by applying various cleaning operations."""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Expand contractions
        text = self._expand_contractions(text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\?\!\,]', '', text)
        
        # Normalize unicode
        text = unicodedata.normalize('NFKD', text)
        
        return text
    
    def _expand_contractions(self, text: str) -> str:
        """Expand common contractions."""
        for contraction, expansion in self.contractions.items():
            text = text.replace(contraction, expansion)
        return text
    
    def clean_for_speech(self, text: str) -> str:
        """Clean text specifically for speech synthesis."""
        # Remove or replace characters that don't sound good in speech
        text = text.replace('&', 'and')
        text = text.replace('@', 'at')
        text = text.replace('#', 'hash')
        text = text.replace('$', 'dollar')
        text = text.replace('%', 'percent')
        text = text.replace('+', 'plus')
        text = text.replace('=', 'equals')
        
        # Clean up numbers for better speech
        text = self._format_numbers_for_speech(text)
        
        return text
    
    def _format_numbers_for_speech(self, text: str) -> str:
        """Format numbers for better speech synthesis."""
        # Convert common number patterns
        text = re.sub(r'\b(\d+):(\d{2})\b', r'\1 \2', text)  # Time format
        text = re.sub(r'\b(\d+)\.(\d+)\b', r'\1 point \2', text)  # Decimals
        text = re.sub(r'\b(\d+)\b', self._number_to_words, text)  # Numbers to words
        
        return text
    
    def _number_to_words(self, match) -> str:
        """Convert numbers to words (simplified)."""
        number = int(match.group())
        
        # Simple number to words conversion
        if number < 20:
            words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
                    'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen',
                    'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
            return words[number] if number < len(words) else str(number)
        elif number < 100:
            tens = ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
            return tens[number // 10 - 2] + (' ' + self._number_to_words(match) if number % 10 else '')
        else:
            return str(number)  # Fallback for larger numbers


class TextAnalyzer:
    """
    Advanced text analysis using NLP techniques.
    Demonstrates tokenization, POS tagging, and feature extraction.
    """
    
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self._download_nltk_data()
    
    def _download_nltk_data(self) -> None:
        """Download required NLTK data."""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        try:
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            nltk.download('averaged_perceptron_tagger')
        
        try:
            nltk.data.find('chunkers/maxent_ne_chunker')
        except LookupError:
            nltk.download('maxent_ne_chunker')
        
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet')
    
    def analyze(self, text: str) -> ProcessedText:
        """Perform comprehensive text analysis."""
        # Tokenize
        tokens = word_tokenize(text)
        
        # POS tagging
        pos_tags = pos_tag(tokens)
        
        # Named entity recognition
        named_entities = self._extract_named_entities(pos_tags)
        
        # Lemmatization
        lemmatized_tokens = [self.lemmatizer.lemmatize(token, pos=self._get_wordnet_pos(tag)) 
                            for token, tag in pos_tags]
        
        # Sentiment analysis (simplified)
        sentiment_score = self._analyze_sentiment(tokens)
        
        # Extract key phrases
        key_phrases = self._extract_key_phrases(tokens, pos_tags)
        
        # Calculate word frequencies
        word_frequencies = Counter(lemmatized_tokens)
        
        return ProcessedText(
            original_text=text,
            cleaned_text=text.lower(),
            tokens=tokens,
            lemmatized_tokens=lemmatized_tokens,
            pos_tags=pos_tags,
            named_entities=named_entities,
            sentiment_score=sentiment_score,
            key_phrases=key_phrases,
            word_frequencies=dict(word_frequencies)
        )
    
    def _extract_named_entities(self, pos_tags: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        """Extract named entities from POS-tagged text."""
        try:
            # Create a simple sentence for NER
            sentence = ' '.join([token for token, _ in pos_tags])
            chunks = ne_chunk(pos_tags)
            
            entities = []
            for chunk in chunks:
                if hasattr(chunk, 'label'):
                    entities.append((' '.join([token for token, _ in chunk.leaves()]), chunk.label()))
            
            return entities
        except Exception:
            return []
    
    def _get_wordnet_pos(self, treebank_tag: str) -> str:
        """Convert POS tag to WordNet format."""
        if treebank_tag.startswith('J'):
            return 'a'  # Adjective
        elif treebank_tag.startswith('V'):
            return 'v'  # Verb
        elif treebank_tag.startswith('N'):
            return 'n'  # Noun
        elif treebank_tag.startswith('R'):
            return 'r'  # Adverb
        else:
            return 'n'  # Default to noun
    
    def _analyze_sentiment(self, tokens: List[str]) -> float:
        """Simple sentiment analysis using word lists."""
        positive_words = {
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
            'awesome', 'brilliant', 'perfect', 'love', 'like', 'enjoy'
        }
        negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'disgusting', 'hate',
            'dislike', 'angry', 'sad', 'disappointed', 'frustrated'
        }
        
        positive_count = sum(1 for token in tokens if token.lower() in positive_words)
        negative_count = sum(1 for token in tokens if token.lower() in negative_words)
        
        total_sentiment_words = positive_count + negative_count
        if total_sentiment_words == 0:
            return 0.0
        
        return (positive_count - negative_count) / total_sentiment_words
    
    def _extract_key_phrases(self, tokens: List[str], pos_tags: List[Tuple[str, str]]) -> List[str]:
        """Extract key phrases using noun phrases and important words."""
        key_phrases = []
        
        # Extract noun phrases (simplified)
        current_phrase = []
        for token, tag in pos_tags:
            if tag.startswith('N'):  # Noun
                current_phrase.append(token)
            else:
                if len(current_phrase) > 1:
                    key_phrases.append(' '.join(current_phrase))
                current_phrase = []
        
        # Add remaining phrase
        if len(current_phrase) > 1:
            key_phrases.append(' '.join(current_phrase))
        
        # Add important individual words (nouns, adjectives, verbs)
        important_words = [token for token, tag in pos_tags 
                          if tag.startswith(('N', 'J', 'V')) and token.lower() not in self.stop_words]
        key_phrases.extend(important_words)
        
        return list(set(key_phrases))  # Remove duplicates


class TextProcessor:
    """
    Main text processing pipeline combining normalization and analysis.
    """
    
    def __init__(self):
        self.normalizer = TextNormalizer()
        self.analyzer = TextAnalyzer()
        self.lock = threading.Lock()
    
    def process(self, text: str, for_speech: bool = False) -> ProcessedText:
        """Process text through the complete pipeline."""
        with self.lock:
            # Normalize text
            if for_speech:
                normalized_text = self.normalizer.clean_for_speech(text)
            else:
                normalized_text = self.normalizer.normalize(text)
            
            # Analyze text
            result = self.analyzer.analyze(normalized_text)
            
            # Update cleaned text
            result.cleaned_text = normalized_text
            
            return result
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract different types of entities from text."""
        processed = self.process(text)
        
        entities = {
            'persons': [],
            'organizations': [],
            'locations': [],
            'dates': [],
            'times': [],
            'numbers': []
        }
        
        # Extract named entities
        for entity, label in processed.named_entities:
            if label == 'PERSON':
                entities['persons'].append(entity)
            elif label == 'ORGANIZATION':
                entities['organizations'].append(entity)
            elif label == 'GPE':  # Geopolitical entity
                entities['locations'].append(entity)
        
        # Extract dates and times using regex
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}\b'
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, text.lower())
            entities['dates'].extend(matches)
        
        time_patterns = [
            r'\b\d{1,2}:\d{2}\s*(am|pm)?\b',
            r'\b\d{1,2}\s*(am|pm)\b'
        ]
        
        for pattern in time_patterns:
            matches = re.findall(pattern, text.lower())
            entities['times'].extend(matches)
        
        # Extract numbers
        number_pattern = r'\b\d+\b'
        numbers = re.findall(number_pattern, text)
        entities['numbers'].extend(numbers)
        
        return entities
    
    def get_text_summary(self, text: str) -> Dict[str, any]:
        """Get a summary of text characteristics."""
        processed = self.process(text)
        
        return {
            'word_count': len(processed.tokens),
            'sentence_count': len(sent_tokenize(text)),
            'unique_words': len(set(processed.lemmatized_tokens)),
            'sentiment': processed.sentiment_score,
            'key_phrases': processed.key_phrases[:5],  # Top 5
            'most_common_words': dict(processed.word_frequencies.most_common(5)),
            'readability_score': self._calculate_readability(text)
        }
    
    def _calculate_readability(self, text: str) -> float:
        """Calculate a simple readability score."""
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        
        if len(sentences) == 0:
            return 0.0
        
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables = sum(self._count_syllables(word) for word in words) / len(words)
        
        # Simple readability formula
        readability = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables)
        return max(0, min(100, readability))
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word (approximation)."""
        word = word.lower()
        vowels = 'aeiouy'
        syllable_count = 0
        prev_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_was_vowel:
                syllable_count += 1
            prev_was_vowel = is_vowel
        
        # Handle silent 'e'
        if word.endswith('e') and syllable_count > 1:
            syllable_count -= 1
        
        return max(1, syllable_count)


if __name__ == "__main__":
    # Demo the text processor
    processor = TextProcessor()
    
    test_text = "Hello! I'm excited to tell you about our amazing new product. It's absolutely fantastic and will revolutionize the industry. The launch date is March 15th, 2024 at 2:30 PM. Contact John Smith at Acme Corp for more details."
    
    print("Original text:")
    print(test_text)
    print("\n" + "="*50)
    
    # Process text
    result = processor.process(test_text)
    
    print("Processed text:")
    print(f"Cleaned: {result.cleaned_text}")
    print(f"Tokens: {result.tokens[:10]}...")  # First 10 tokens
    print(f"Lemmatized: {result.lemmatized_tokens[:10]}...")
    print(f"POS tags: {result.pos_tags[:5]}...")  # First 5 POS tags
    print(f"Named entities: {result.named_entities}")
    print(f"Sentiment score: {result.sentiment_score:.2f}")
    print(f"Key phrases: {result.key_phrases}")
    
    print("\n" + "="*50)
    
    # Extract entities
    entities = processor.extract_entities(test_text)
    print("Extracted entities:")
    for entity_type, entity_list in entities.items():
        if entity_list:
            print(f"  {entity_type}: {entity_list}")
    
    print("\n" + "="*50)
    
    # Get text summary
    summary = processor.get_text_summary(test_text)
    print("Text summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*50)
    
    # Test speech cleaning
    speech_text = "The price is $99.99 & it's 50% off! Call us at 555-1234."
    cleaned_speech = processor.normalizer.clean_for_speech(speech_text)
    print(f"Speech cleaning:")
    print(f"Original: {speech_text}")
    print(f"Cleaned: {cleaned_speech}")




