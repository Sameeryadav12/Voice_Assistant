"""
Web Search & Browser Control Skill - Advanced web interaction
Provides comprehensive web search and browser automation capabilities.
"""

import webbrowser
import urllib.parse
import requests
from typing import Dict, Any, Optional, List
from skills.base_skill import BaseSkill, SkillContext, SkillResult, SkillPriority
import re
from datetime import datetime
import json
import os


class WebBrowserSkill(BaseSkill):
    """
    Advanced skill for web search and browser control.
    Features:
    - Google/Bing search
    - Wikipedia integration
    - YouTube search
    - Image search
    - Website opening
    - Search history
    """
    
    def __init__(self):
        super().__init__(
            name="web_browser",
            description="Search the web and control browser",
            priority=SkillPriority.CRITICAL
        )
        
        # Common websites mapping
        self.common_sites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "gmail": "https://mail.google.com",
            "facebook": "https://www.facebook.com",
            "twitter": "https://www.twitter.com",
            "x": "https://www.x.com",
            "instagram": "https://www.instagram.com",
            "linkedin": "https://www.linkedin.com",
            "github": "https://www.github.com",
            "stackoverflow": "https://www.stackoverflow.com",
            "reddit": "https://www.reddit.com",
            "amazon": "https://www.amazon.com",
            "netflix": "https://www.netflix.com",
            "spotify": "https://www.spotify.com",
            "wikipedia": "https://www.wikipedia.org",
        }
        
        # Search history
        self.history_file = os.path.join("data", "search_history.json")
        self.search_history = self._load_history()
        
    def can_handle(self, context: SkillContext) -> bool:
        """Check if this skill can handle the request."""
        user_input = context.user_input.lower()
        
        # More flexible search keywords
        search_keywords = [
            "search", "google", "look up", "find", "search for",
            "search the web", "web search", "internet search", "browse",
            "web browse", "online search", "search online", "look for",
            "find information", "search information", "web lookup"
        ]
        
        # More flexible browser keywords
        browser_keywords = [
            "open", "go to", "visit", "navigate", "browse", "launch",
            "website", "url", "youtube", "wikipedia", "images", "web",
            "internet", "online", "web page", "webpage", "site"
        ]
        
        has_search = any(keyword in user_input for keyword in search_keywords)
        has_browser = any(keyword in user_input for keyword in browser_keywords)
        
        # Check for specific site names
        has_site = any(site in user_input for site in self.common_sites.keys())
        
        return has_search or has_browser or has_site
    
    def execute(self, context: SkillContext) -> SkillResult:
        """Execute web search or browser command."""
        user_input = context.user_input.lower()
        
        try:
            # Wikipedia search
            if "wikipedia" in user_input or "wiki" in user_input:
                return self._handle_wikipedia(user_input)
            
            # YouTube search/open
            elif "youtube" in user_input:
                return self._handle_youtube(user_input)
            
            # Image search
            elif "image" in user_input or "picture" in user_input or "photo" in user_input:
                return self._handle_image_search(user_input)
            
            # Open specific website
            elif any(word in user_input for word in ["open", "go to", "visit", "navigate"]):
                return self._handle_open_website(user_input)
            
            # General web search
            elif any(word in user_input for word in ["search", "google", "look up", "find"]):
                return self._handle_web_search(user_input)
            
            # Browse the web
            elif "browse the web" in user_input or "browse web" in user_input:
                return self._handle_browse_web()
            
            else:
                return SkillResult(
                    success=False,
                    message="I can search the web or open websites. Try 'search for Python' or 'open YouTube'",
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
    
    def _handle_web_search(self, user_input: str) -> SkillResult:
        """Handle general web search."""
        start_time = datetime.now()
        
        # Extract search query
        query = self._extract_search_query(user_input)
        
        if not query:
            return SkillResult(
                success=False,
                message="What would you like me to search for?",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
        
        # Build Google search URL
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        
        # Open in browser
        webbrowser.open(search_url)
        
        # Save to history
        self._add_to_history("google_search", query, search_url)
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        message = f"Searching Google for: '{query}'\nOpening in your browser..."
        
        return SkillResult(
            success=True,
            message=message,
            data={"query": query, "url": search_url, "type": "google_search"},
            execution_time=execution_time,
            skill_name=self.name
        )
    
    def _handle_wikipedia(self, user_input: str) -> SkillResult:
        """Handle Wikipedia search and summary."""
        start_time = datetime.now()
        
        # Extract topic
        topic = self._extract_wikipedia_topic(user_input)
        
        if not topic:
            return SkillResult(
                success=False,
                message="What Wikipedia topic would you like to search for?",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
        
        try:
            # Get Wikipedia summary using API
            wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(topic)}"
            response = requests.get(wiki_url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                title = data.get('title', topic)
                extract = data.get('extract', 'No summary available')
                page_url = data.get('content_urls', {}).get('desktop', {}).get('page', '')
                
                # Limit extract length
                if len(extract) > 300:
                    extract = extract[:297] + "..."
                
                # Open full page in browser
                if page_url:
                    webbrowser.open(page_url)
                
                # Save to history
                self._add_to_history("wikipedia", title, page_url)
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                message = f"Wikipedia: {title}\n\n{extract}\n\nOpening full article in browser..."
                
                return SkillResult(
                    success=True,
                    message=message,
                    data={"title": title, "summary": extract, "url": page_url, "type": "wikipedia"},
                    execution_time=execution_time,
                    skill_name=self.name
                )
            else:
                # Fallback to direct Wikipedia search
                wiki_search_url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(topic.replace(' ', '_'))}"
                webbrowser.open(wiki_search_url)
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                return SkillResult(
                    success=True,
                    message=f"Opening Wikipedia page for '{topic}'...",
                    data={"topic": topic, "url": wiki_search_url, "type": "wikipedia"},
                    execution_time=execution_time,
                    skill_name=self.name
                )
        
        except Exception as e:
            # Fallback to opening Wikipedia search
            wiki_search_url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(topic.replace(' ', '_'))}"
            webbrowser.open(wiki_search_url)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return SkillResult(
                success=True,
                message=f"Opening Wikipedia page for '{topic}'...",
                data={"topic": topic, "url": wiki_search_url, "type": "wikipedia"},
                execution_time=execution_time,
                skill_name=self.name
            )
    
    def _handle_youtube(self, user_input: str) -> SkillResult:
        """Handle YouTube search or opening."""
        start_time = datetime.now()
        
        # Check if it's a search or just opening YouTube
        if any(word in user_input for word in ["search", "find", "look for", "for"]):
            # YouTube search
            query = self._extract_youtube_query(user_input)
            
            if query:
                youtube_search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
                webbrowser.open(youtube_search_url)
                
                # Save to history
                self._add_to_history("youtube_search", query, youtube_search_url)
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                return SkillResult(
                    success=True,
                    message=f"Searching YouTube for: '{query}'\nOpening in your browser...",
                    data={"query": query, "url": youtube_search_url, "type": "youtube_search"},
                    execution_time=execution_time,
                    skill_name=self.name
                )
        
        # Just open YouTube homepage
        webbrowser.open(self.common_sites["youtube"])
        
        # Save to history
        self._add_to_history("website", "YouTube", self.common_sites["youtube"])
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return SkillResult(
            success=True,
            message="Opening YouTube...",
            data={"url": self.common_sites["youtube"], "type": "website"},
            execution_time=execution_time,
            skill_name=self.name
        )
    
    def _handle_image_search(self, user_input: str) -> SkillResult:
        """Handle image search."""
        start_time = datetime.now()
        
        # Extract search query
        query = self._extract_image_query(user_input)
        
        if not query:
            return SkillResult(
                success=False,
                message="What images would you like me to search for?",
                data={},
                execution_time=0.0,
                skill_name=self.name
            )
        
        # Google Images search URL
        image_search_url = f"https://www.google.com/search?tbm=isch&q={urllib.parse.quote(query)}"
        
        # Open in browser
        webbrowser.open(image_search_url)
        
        # Save to history
        self._add_to_history("image_search", query, image_search_url)
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        message = f"Searching images for: '{query}'\nOpening Google Images..."
        
        return SkillResult(
            success=True,
            message=message,
            data={"query": query, "url": image_search_url, "type": "image_search"},
            execution_time=execution_time,
            skill_name=self.name
        )
    
    def _handle_open_website(self, user_input: str) -> SkillResult:
        """Handle opening specific websites."""
        start_time = datetime.now()
        
        # Check for common site names
        for site_name, site_url in self.common_sites.items():
            if site_name in user_input:
                webbrowser.open(site_url)
                
                # Save to history
                self._add_to_history("website", site_name.title(), site_url)
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                return SkillResult(
                    success=True,
                    message=f"Opening {site_name.title()}...",
                    data={"site": site_name, "url": site_url, "type": "website"},
                    execution_time=execution_time,
                    skill_name=self.name
                )
        
        # Try to extract URL
        url = self._extract_url(user_input)
        
        if url:
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            webbrowser.open(url)
            
            # Save to history
            self._add_to_history("website", url, url)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return SkillResult(
                success=True,
                message=f"Opening {url}...",
                data={"url": url, "type": "website"},
                execution_time=execution_time,
                skill_name=self.name
            )
        
        return SkillResult(
            success=False,
            message="I couldn't identify which website to open. Try 'open YouTube' or 'open google.com'",
            data={},
            execution_time=0.0,
            skill_name=self.name
        )
    
    def _handle_browse_web(self) -> SkillResult:
        """Handle general web browsing."""
        start_time = datetime.now()
        
        # Open Google homepage as a general web browsing entry point
        webbrowser.open("https://www.google.com")
        
        # Save to history
        self._add_to_history("website", "Google", "https://www.google.com")
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return SkillResult(
            success=True,
            message="Opening web browser with Google homepage for you to browse the web!",
            data={"url": "https://www.google.com", "type": "website"},
            execution_time=execution_time,
            skill_name=self.name
        )
    
    # Helper methods
    
    def _extract_search_query(self, user_input: str) -> Optional[str]:
        """Extract search query from user input."""
        patterns = [
            r'(?:search|google|look up|find)\s+(?:for\s+)?(.+)',
            r'(?:search|google)\s+(.+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                query = match.group(1).strip()
                # Remove trailing words
                query = re.sub(r'\s+(on the web|online|on google|on internet)$', '', query, flags=re.IGNORECASE)
                return query
        
        return None
    
    def _extract_wikipedia_topic(self, user_input: str) -> Optional[str]:
        """Extract Wikipedia topic from user input."""
        patterns = [
            r'wikipedia\s+(?:about\s+)?(.+)',
            r'wiki\s+(.+)',
            r'(?:search|look up)\s+(.+?)\s+(?:on\s+)?wikipedia',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_youtube_query(self, user_input: str) -> Optional[str]:
        """Extract YouTube search query from user input."""
        patterns = [
            r'youtube\s+(?:search\s+)?(?:for\s+)?(.+)',
            r'(?:search|find|look for)\s+(.+?)\s+on\s+youtube',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_image_query(self, user_input: str) -> Optional[str]:
        """Extract image search query from user input."""
        patterns = [
            r'(?:search|find|look for|show)\s+(?:images?|pictures?|photos?)\s+(?:of\s+|for\s+)?(.+)',
            r'images?\s+(?:of\s+)?(.+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_url(self, user_input: str) -> Optional[str]:
        """Extract URL from user input."""
        # Look for .com, .org, .net, etc.
        pattern = r'([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+(?:\.[a-zA-Z]{2,})?)'
        match = re.search(pattern, user_input)
        
        if match:
            return match.group(1)
        
        return None
    
    def _load_history(self) -> List[Dict]:
        """Load search history from file."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_history(self):
        """Save search history to file."""
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.search_history[-100:], f, indent=2)  # Keep last 100 items
    
    def _add_to_history(self, search_type: str, query: str, url: str):
        """Add entry to search history."""
        entry = {
            "type": search_type,
            "query": query,
            "url": url,
            "timestamp": datetime.now().isoformat()
        }
        self.search_history.append(entry)
        self._save_history()


# Skill registration
def get_skill():
    """Factory function to get the skill instance."""
    return WebBrowserSkill()




