"""
Weather and News Skill - Advanced information retrieval
Provides real-time weather forecasts and latest news headlines.
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from skills.base_skill import BaseSkill, SkillContext, SkillResult, SkillPriority
import re


class WeatherNewsSkill(BaseSkill):
    """
    Advanced skill for weather forecasts and news headlines.
    Features:
    - Real-time weather data with forecasts
    - Location-based weather queries
    - Latest news from multiple categories
    - Intelligent caching to reduce API calls
    - Beautiful formatted responses
    """
    
    def __init__(self):
        super().__init__(
            name="weather_news",
            description="Get weather forecasts and news headlines",
            priority=SkillPriority.HIGH
        )
        
        # API Configuration - Using free APIs
        self.weather_api_key = "f9e3c3e6c3c3e6c3c3e6c3c3e6c3c3e6"  # Placeholder - will use wttr.in (no key needed)
        self.news_api_key = "YOUR_NEWS_API_KEY"  # Get free key from newsapi.org
        
        # Cache for reducing API calls
        self.weather_cache = {}
        self.news_cache = {}
        self.cache_duration = 600  # 10 minutes
        
        # Default location - will try to detect current location
        self.default_location = None
        
    def can_handle(self, context: SkillContext) -> bool:
        """Check if this skill can handle the request."""
        user_input = context.user_input.lower()
        
        # Weather keywords - more specific to avoid conflicts
        weather_keywords = [
            "weather", "temperature", "temp", "forecast", 
            "hot", "cold", "rain", "sunny", "climate",
            "degrees", "celsius", "fahrenheit", "what's the weather",
            "how's the weather", "weather today", "current weather",
            "weather in", "forecast for", "temperature in"
        ]
        
        # News keywords
        news_keywords = [
            "news", "headlines", "latest news", "what's happening",
            "current events", "breaking news", "today's news",
            "tech news", "sports news", "business news"
        ]
        
        has_weather = any(keyword in user_input for keyword in weather_keywords)
        has_news = any(keyword in user_input for keyword in news_keywords)
        
        # Be more specific - require actual weather/news context
        if "show" in user_input and not has_weather and not has_news:
            return False
        
        # Don't match if it's about templates, contacts, or other non-weather topics
        non_weather_keywords = ["template", "contact", "message", "whatsapp", "email", "calendar", "schedule"]
        if any(keyword in user_input for keyword in non_weather_keywords):
            return False
        
        return has_weather or has_news
    
    def execute(self, context: SkillContext) -> SkillResult:
        """Execute weather or news query."""
        user_input = context.user_input.lower()
        
        try:
            # Determine if it's weather or news
            if any(word in user_input for word in ["weather", "temperature", "temp", "forecast", "climate"]):
                return self._handle_weather(user_input)
            elif any(word in user_input for word in ["news", "headlines", "current events", "breaking"]):
                return self._handle_news(user_input)
            else:
                return SkillResult(
                    success=False,
                    message="I can help with weather and news. Try 'what's the weather?' or 'give me the news'",
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
    
    def _handle_weather(self, user_input: str) -> SkillResult:
        """Handle weather queries."""
        start_time = datetime.now()
        
        # Extract location from input
        location = self._extract_location(user_input)
        if not location:
            location = self._get_current_location()
        
        # Check cache first
        cache_key = f"weather_{location.lower()}"
        if cache_key in self.weather_cache:
            cached_data, cache_time = self.weather_cache[cache_key]
            if (datetime.now() - cache_time).seconds < self.cache_duration:
                execution_time = (datetime.now() - start_time).total_seconds()
                return SkillResult(
                    success=True,
                    message=cached_data['message'],
                    data=cached_data,
                    execution_time=execution_time,
                    skill_name=self.name
                )
        
        # Fetch weather data
        weather_data = self._fetch_weather(location)
        
        if weather_data:
            # Cache the result
            self.weather_cache[cache_key] = (weather_data, datetime.now())
            
            execution_time = (datetime.now() - start_time).total_seconds()
            return SkillResult(
                success=True,
                message=weather_data['message'],
                data=weather_data,
                execution_time=execution_time,
                skill_name=self.name
            )
        else:
            return SkillResult(
                success=False,
                message=f"Sorry, I couldn't fetch weather data for {location}",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error="API fetch failed"
            )
    
    def _handle_news(self, user_input: str) -> SkillResult:
        """Handle news queries."""
        start_time = datetime.now()
        
        # Extract category from input
        category = self._extract_news_category(user_input)
        
        # Check cache
        cache_key = f"news_{category}"
        if cache_key in self.news_cache:
            cached_data, cache_time = self.news_cache[cache_key]
            if (datetime.now() - cache_time).seconds < self.cache_duration:
                execution_time = (datetime.now() - start_time).total_seconds()
                return SkillResult(
                    success=True,
                    message=cached_data['message'],
                    data=cached_data,
                    execution_time=execution_time,
                    skill_name=self.name
                )
        
        # Fetch news data
        news_data = self._fetch_news(category)
        
        if news_data:
            # Cache the result
            self.news_cache[cache_key] = (news_data, datetime.now())
            
            execution_time = (datetime.now() - start_time).total_seconds()
            return SkillResult(
                success=True,
                message=news_data['message'],
                data=news_data,
                execution_time=execution_time,
                skill_name=self.name
            )
        else:
            return SkillResult(
                success=False,
                message="Sorry, I couldn't fetch the latest news",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error="News fetch failed"
            )
    
    def _fetch_weather(self, location: str) -> Optional[Dict]:
        """Fetch weather data using wttr.in (free, no API key needed)."""
        try:
            # Using wttr.in - a free weather service
            url = f"https://wttr.in/{location}?format=j1"
            
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract current weather
                current = data['current_condition'][0]
                location_name = data['nearest_area'][0]['areaName'][0]['value']
                country = data['nearest_area'][0]['country'][0]['value']
                
                # Get forecast for today
                today_forecast = data['weather'][0]
                
                # Build response
                temp_c = current['temp_C']
                temp_f = current['temp_F']
                feels_like_c = current['FeelsLikeC']
                feels_like_f = current['FeelsLikeF']
                humidity = current['humidity']
                condition = current['weatherDesc'][0]['value']
                wind_speed = current['windspeedKmph']
                
                # Forecast data
                max_temp_c = today_forecast['maxtempC']
                min_temp_c = today_forecast['mintempC']
                max_temp_f = today_forecast['maxtempF']
                min_temp_f = today_forecast['mintempF']
                
                message = f"🌤️ Weather for {location_name}, {country}:\n\n"
                message += f"Current: {temp_c}°C ({temp_f}°F) - {condition}\n"
                message += f"Feels like: {feels_like_c}°C ({feels_like_f}°F)\n"
                message += f"Today's Range: {min_temp_c}°C to {max_temp_c}°C ({min_temp_f}°F to {max_temp_f}°F)\n"
                message += f"Humidity: {humidity}%\n"
                message += f"Wind Speed: {wind_speed} km/h"
                
                return {
                    'message': message,
                    'location': location_name,
                    'country': country,
                    'temperature_c': temp_c,
                    'temperature_f': temp_f,
                    'feels_like_c': feels_like_c,
                    'feels_like_f': feels_like_f,
                    'condition': condition,
                    'humidity': humidity,
                    'wind_speed': wind_speed,
                    'max_temp_c': max_temp_c,
                    'min_temp_c': min_temp_c,
                    'max_temp_f': max_temp_f,
                    'min_temp_f': min_temp_f
                }
            
            return None
            
        except Exception as e:
            print(f"Weather fetch error: {e}")
            return None
    
    def _fetch_news(self, category: str = "general") -> Optional[Dict]:
        """Fetch news headlines using free RSS feeds (no API key needed)."""
        try:
            # Using Google News RSS (free, no API key)
            # Categories: world, nation, business, technology, entertainment, sports, science, health
            
            if category in ["tech", "technology"]:
                url = "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB"
            elif category in ["business"]:
                url = "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB"
            elif category in ["sports"]:
                url = "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtVnVHZ0pWVXlnQVAB"
            elif category in ["entertainment"]:
                url = "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FtVnVHZ0pWVXlnQVAB"
            elif category in ["science"]:
                url = "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp0Y1RjU0FtVnVHZ0pWVXlnQVAB"
            else:  # world/general
                url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
            
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                # Parse RSS feed (simple XML parsing)
                import xml.etree.ElementTree as ET
                
                root = ET.fromstring(response.content)
                
                headlines = []
                for item in root.findall('.//item')[:5]:  # Get top 5 headlines
                    title = item.find('title')
                    pub_date = item.find('pubDate')
                    
                    if title is not None:
                        headlines.append({
                            'title': title.text,
                            'published': pub_date.text if pub_date is not None else 'Recently'
                        })
                
                if headlines:
                    message = f"📰 Latest {category.title()} News:\n\n"
                    for i, headline in enumerate(headlines, 1):
                        message += f"{i}. {headline['title']}\n"
                    
                    return {
                        'message': message.strip(),
                        'category': category,
                        'headlines': headlines,
                        'count': len(headlines)
                    }
            
            return None
            
        except Exception as e:
            print(f"News fetch error: {e}")
            return None
    
    def _extract_location(self, user_input: str) -> Optional[str]:
        """Extract location from user input."""
        # Common patterns: "weather in London", "London weather", "what's the weather in Paris"
        patterns = [
            r'weather\s+in\s+([a-zA-Z\s]+)',
            r'in\s+([a-zA-Z\s]+)\s+weather',
            r'forecast\s+for\s+([a-zA-Z\s]+)',
            r'temperature\s+in\s+([a-zA-Z\s]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                # Remove common filler words
                location = location.replace(' today', '').replace(' now', '').replace(' currently', '')
                return location
        
        # Check for standalone city names (simple approach)
        common_cities = [
            "london", "paris", "tokyo", "new york", "los angeles", "chicago",
            "houston", "phoenix", "philadelphia", "san diego", "dallas", "miami",
            "boston", "seattle", "washington", "atlanta", "denver", "portland"
        ]
        
        for city in common_cities:
            if city in user_input:
                return city.title()
        
        return None
    
    def _get_current_location(self) -> str:
        """Get user's current location using IP geolocation."""
        try:
            # Use a free IP geolocation service
            response = requests.get("http://ip-api.com/json/", timeout=3)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    city = data.get('city', 'Unknown')
                    country = data.get('country', 'Unknown')
                    return f"{city}, {country}"
        except Exception as e:
            print(f"Location detection error: {e}")
        
        # Fallback to a generic location
        return "New York, USA"
    
    def _extract_news_category(self, user_input: str) -> str:
        """Extract news category from user input."""
        if any(word in user_input for word in ["tech", "technology"]):
            return "technology"
        elif "business" in user_input:
            return "business"
        elif "sports" in user_input:
            return "sports"
        elif "entertainment" in user_input or "entertainment" in user_input:
            return "entertainment"
        elif "science" in user_input:
            return "science"
        else:
            return "general"


# Skill registration
def get_skill():
    """Factory function to get the skill instance."""
    return WeatherNewsSkill()

