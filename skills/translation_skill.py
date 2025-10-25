"""
Translation & Multi-Language Skill - Language translation and support
Provides comprehensive translation capabilities and multi-language support.
"""

import requests
import urllib.parse
from typing import Dict, Any, Optional
from skills.base_skill import BaseSkill, SkillContext, SkillResult, SkillPriority
import re


class TranslationSkill(BaseSkill):
    """
    Advanced skill for language translation and multi-language support.
    Features:
    - Text translation between languages
    - Language detection
    - Common phrases in multiple languages
    - Pronunciation guides
    """
    
    def __init__(self):
        super().__init__(
            name="translation",
            description="Translate text between languages",
            priority=SkillPriority.CRITICAL
        )
        
        # Language codes mapping
        self.languages = {
            "spanish": "es", "french": "fr", "german": "de", "italian": "it",
            "portuguese": "pt", "russian": "ru", "japanese": "ja", "chinese": "zh-CN",
            "korean": "ko", "arabic": "ar", "hindi": "hi", "dutch": "nl",
            "swedish": "sv", "turkish": "tr", "polish": "pl", "vietnamese": "vi",
            "indonesian": "id", "thai": "th", "greek": "el", "czech": "cs",
            "danish": "da", "finnish": "fi", "hebrew": "he", "norwegian": "no",
            "romanian": "ro", "ukrainian": "uk", "english": "en"
        }
        
        # Common phrases database
        self.common_phrases = {
            "hello": {
                "spanish": "Hola", "french": "Bonjour", "german": "Hallo",
                "italian": "Ciao", "portuguese": "Olá", "russian": "Привет",
                "japanese": "こんにちは", "chinese": "你好", "korean": "안녕하세요"
            },
            "thank you": {
                "spanish": "Gracias", "french": "Merci", "german": "Danke",
                "italian": "Grazie", "portuguese": "Obrigado", "russian": "Спасибо",
                "japanese": "ありがとう", "chinese": "谢谢", "korean": "감사합니다"
            },
            "goodbye": {
                "spanish": "Adiós", "french": "Au revoir", "german": "Auf Wiedersehen",
                "italian": "Arrivederci", "portuguese": "Tchau", "russian": "До свидания",
                "japanese": "さようなら", "chinese": "再见", "korean": "안녕히 가세요"
            },
            "yes": {
                "spanish": "Sí", "french": "Oui", "german": "Ja",
                "italian": "Sì", "portuguese": "Sim", "russian": "Да",
                "japanese": "はい", "chinese": "是", "korean": "네"
            },
            "no": {
                "spanish": "No", "french": "Non", "german": "Nein",
                "italian": "No", "portuguese": "Não", "russian": "Нет",
                "japanese": "いいえ", "chinese": "不", "korean": "아니요"
            }
        }
        
    def can_handle(self, context: SkillContext) -> bool:
        """Check if this skill can handle the request."""
        user_input = context.user_input.lower()
        
        # More flexible translation keywords
        translation_keywords = [
            "translate", "translation", "how do you say", "what is",
            "in spanish", "in french", "in german", "in italian",
            "to spanish", "to french", "to german", "to italian",
            "language", "say in", "convert to", "change to",
            "speak", "pronounce", "meaning", "word", "phrase",
            "learn", "teach me", "help me say", "how to say"
        ]
        
        # Check for any language name
        has_language = any(lang in user_input for lang in self.languages.keys())
        has_translation = any(keyword in user_input for keyword in translation_keywords)
        
        return has_translation or has_language
    
    def execute(self, context: SkillContext) -> SkillResult:
        """Execute translation command."""
        user_input = context.user_input.lower()
        
        try:
            # Handle common phrase queries
            if any(word in user_input for word in ["how do you say", "what is"]):
                return self._handle_common_phrase(user_input)
            
            # Handle translation requests
            elif "translate" in user_input:
                return self._handle_translation(user_input)
            
            # Handle language learning
            elif any(word in user_input for word in ["teach me", "learn", "speak"]):
                return self._handle_language_learning(user_input)
            
            else:
                return SkillResult(
                    success=False,
                    message="I can translate text! Try 'translate hello to Spanish' or 'how do you say thank you in French?'",
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
    
    def _handle_common_phrase(self, user_input: str) -> SkillResult:
        """Handle common phrase translations."""
        # Extract phrase and target language
        phrase = self._extract_phrase(user_input)
        target_lang = self._extract_language(user_input)
        
        if not phrase or not target_lang:
            return SkillResult(
                success=False,
                message="Please specify what phrase and which language. Try 'how do you say hello in Spanish?'",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
        
        # Check common phrases database
        phrase_lower = phrase.lower()
        if phrase_lower in self.common_phrases:
            if target_lang in self.common_phrases[phrase_lower]:
                translation = self.common_phrases[phrase_lower][target_lang]
                
                message = f"'{phrase.title()}' in {target_lang.title()}: '{translation}'"
                
                # Add pronunciation guide for some languages
                if target_lang == "japanese":
                    message += "\n(Pronunciation: Romanized as shown)"
                
                return SkillResult(
                    success=True,
                    message=message,
                    data={"phrase": phrase, "translation": translation, "language": target_lang},
                    execution_time=0.0,
                    skill_name=self.name
                )
        
        # Fall back to API translation
        return self._translate_text(phrase, target_lang, "en")
    
    def _handle_translation(self, user_input: str) -> SkillResult:
        """Handle general translation requests."""
        # Extract text to translate
        text = self._extract_translation_text(user_input)
        
        # Extract source and target languages
        target_lang = self._extract_language(user_input)
        source_lang = "auto"  # Auto-detect source language
        
        if not text:
            return SkillResult(
                success=False,
                message="What would you like me to translate?",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
        
        if not target_lang:
            return SkillResult(
                success=False,
                message="Which language should I translate to? Try 'translate hello to Spanish'",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
        
        return self._translate_text(text, target_lang, source_lang)
    
    def _handle_language_learning(self, user_input: str) -> SkillResult:
        """Handle language learning requests."""
        target_lang = self._extract_language(user_input)
        
        if not target_lang:
            return SkillResult(
                success=False,
                message="Which language would you like to learn?",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
        
        # Provide basic phrases
        message = f"Basic {target_lang.title()} Phrases:\n\n"
        
        basic_phrases = ["hello", "thank you", "goodbye", "yes", "no"]
        
        for phrase in basic_phrases:
            if phrase in self.common_phrases and target_lang in self.common_phrases[phrase]:
                translation = self.common_phrases[phrase][target_lang]
                message += f"• {phrase.title()}: {translation}\n"
        
        message += f"\nAsk me 'how do you say [phrase] in {target_lang}' to learn more!"
        
        return SkillResult(
            success=True,
            message=message,
            data={"language": target_lang, "phrases": basic_phrases},
            execution_time=0.0,
            skill_name=self.name
        )
    
    def _translate_text(self, text: str, target_lang: str, source_lang: str = "auto") -> SkillResult:
        """Translate text using API."""
        try:
            # Get language code
            target_code = self.languages.get(target_lang, target_lang)
            
            # Using MyMemory Translation API (free, no API key needed)
            url = f"https://api.mymemory.translated.net/get"
            params = {
                "q": text,
                "langpair": f"{source_lang}|{target_code}"
            }
            
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                if "responseData" in data and "translatedText" in data["responseData"]:
                    translation = data["responseData"]["translatedText"]
                    
                    # Detect if translation is same as input (might mean translation failed)
                    if translation.lower() == text.lower():
                        message = f"Could not translate '{text}' to {target_lang.title()}. It might already be in that language!"
                    else:
                        message = f"Translation to {target_lang.title()}:\n\n"
                        message += f"Original: '{text}'\n"
                        message += f"Translation: '{translation}'"
                    
                    return SkillResult(
                        success=True,
                        message=message,
                        data={"original": text, "translation": translation, "target_language": target_lang},
                        execution_time=0.0,
                        skill_name=self.name
                    )
            
            # Fallback message
            return SkillResult(
                success=False,
                message=f"Sorry, I couldn't translate that to {target_lang.title()}",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
        
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Translation error: {str(e)}",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error=str(e)
            )
    
    def _extract_phrase(self, user_input: str) -> Optional[str]:
        """Extract phrase to translate from user input."""
        patterns = [
            r'how do you say\s+["\']?([^"\']+?)["\']?\s+in',
            r'what is\s+["\']?([^"\']+?)["\']?\s+in',
            r'say\s+["\']?([^"\']+?)["\']?\s+in'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_translation_text(self, user_input: str) -> Optional[str]:
        """Extract text to translate from user input."""
        patterns = [
            r'translate\s+["\']?([^"\']+?)["\']?\s+to',
            r'translate\s+(.+?)\s+to',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_language(self, user_input: str) -> Optional[str]:
        """Extract target language from user input."""
        # Check for "in [language]" or "to [language]"
        for lang_name in self.languages.keys():
            if f"in {lang_name}" in user_input or f"to {lang_name}" in user_input:
                return lang_name
        
        # Check for just language name
        for lang_name in self.languages.keys():
            if lang_name in user_input:
                return lang_name
        
        return None


# Skill registration
def get_skill():
    """Factory function to get the skill instance."""
    return TranslationSkill()




