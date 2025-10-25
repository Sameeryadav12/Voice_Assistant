"""
File management skill using graph-based search algorithms.
Demonstrates integration with file system operations and search algorithms.
"""

import os
import glob
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from skills.base_skill import BaseSkill, SkillContext, SkillResult, SkillPriority
from core.graph_search import FileSystemGraph, ApplicationLauncher


class FileSearchSkill(BaseSkill):
    """
    Skill for searching and managing files using graph-based algorithms.
    Demonstrates integration with advanced search algorithms.
    """
    
    def __init__(self, fs_graph: FileSystemGraph):
        super().__init__(
            name="file_search",
            description="Search and manage files using advanced algorithms",
            priority=SkillPriority.CRITICAL
        )
        self.fs_graph = fs_graph
        self.triggers = ["find", "search", "file", "locate", "where is"]
        self.required_entities = []
        self.optional_entities = ["filename", "filetype", "location", "content"]
        
        # Common file type mappings
        self.file_type_mappings = {
            'document': ['.pdf', '.doc', '.docx', '.txt', '.rtf'],
            'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
            'video': ['.mp4', '.avi', '.mov', '.wmv', '.flv'],
            'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
            'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c'],
            'spreadsheet': ['.xls', '.xlsx', '.csv'],
            'presentation': ['.ppt', '.pptx']
        }
    
    def can_handle(self, context: SkillContext) -> bool:
        """Check if this skill can handle file operations."""
        user_input = context.user_input.lower()
        
        # More flexible file keywords
        file_keywords = [
            "find", "search", "file", "locate", "where is", "open file",
            "show files", "list files", "browse", "explore", "look for",
            "find files", "search files", "locate files", "file search",
            "open", "show me files", "display files", "file explorer",
            "open file", "open files", "file named", "file called"
        ]
        
        # Exclude web-related commands
        web_keywords = [
            "python tutorials", "youtube", "images of cats", "browse the web",
            "browse web", "search for", "open youtube", "search images", 
            "web search", "internet search", "google", "wikipedia", "online"
        ]
        
        # Check if it's a web command
        if any(web_keyword in user_input for web_keyword in web_keywords):
            return False
            
        return any(keyword in user_input for keyword in file_keywords)
    
    def execute(self, context: SkillContext) -> SkillResult:
        """Execute file search operation."""
        try:
            user_input = context.user_input.lower()
            
            # Determine operation type
            if any(keyword in user_input for keyword in ["list files", "show files", "files in", "directory", "folder"]):
                return self._handle_file_list(context)
            elif "open file" in user_input or ("open" in user_input and any(ext in user_input for ext in [".py", ".txt", ".doc", ".pdf", ".jpg", ".png", ".mp4", ".mp3"])):
                return self._handle_file_open(context)
            elif any(keyword in user_input for keyword in ["find", "search", "locate", "where is"]):
                return self._handle_file_search(context)
            else:
                return self._handle_file_search(context)  # Default to search
        
        except Exception as e:
            return SkillResult(
                success=False,
                message="Sorry, I had trouble with the file operation.",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error=str(e)
            )
    
    def _handle_file_search(self, context: SkillContext) -> SkillResult:
        """Handle file search operations."""
        # Extract search query
        query = self._extract_search_query(context.user_input)
        
        if not query:
            return SkillResult(
                success=False,
                message="What would you like me to search for?",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error="No search query"
            )
        
        # Determine search type
        search_type = self._determine_search_type(context.user_input)
        
        # Perform search
        if search_type == "name":
            results = self._search_by_name(query)
        elif search_type == "content":
            results = self._search_by_content(query)
        elif search_type == "type":
            results = self._search_by_type(query)
        else:
            results = self._search_by_name(query)  # Default
        
        if not results:
            return SkillResult(
                success=True,
                message=f"I couldn't find any files matching '{query}'.",
                data={'results': []},
                execution_time=0.0,
                skill_name=self.name
            )
        
        # Format results
        result_list = []
        for i, file_node in enumerate(results[:10]):  # Limit to 10 results
            file_info = {
                'name': file_node.name,
                'path': file_node.path,
                'type': file_node.node_type,
                'size': file_node.size,
                'modified': file_node.last_modified
            }
            result_list.append(file_info)
        
        # Create response message
        if len(results) == 1:
            response = f"I found 1 file: {result_list[0]['name']} at {result_list[0]['path']}"
        else:
            response = f"I found {len(results)} files matching '{query}':\n"
            for i, file_info in enumerate(result_list[:5]):  # Show first 5
                response += f"{i+1}. {file_info['name']} at {file_info['path']}\n"
            if len(results) > 5:
                response += f"... and {len(results) - 5} more files"
        
        return SkillResult(
            success=True,
            message=response,
            data={'results': result_list, 'total_found': len(results)},
            execution_time=0.0,
            skill_name=self.name
        )
    
    def _handle_file_open(self, context: SkillContext) -> SkillResult:
        """Handle opening files."""
        query = self._extract_search_query(context.user_input)
        
        if not query:
            return SkillResult(
                success=False,
                message="What file would you like me to open?",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error="No file specified"
            )
        
        # Search for the file
        results = self._search_by_name(query)
        
        if not results:
            return SkillResult(
                success=False,
                message=f"I couldn't find a file matching '{query}'.",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error="File not found"
            )
        
        # Try to open the first result
        file_path = results[0].path
        
        try:
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            elif os.name == 'posix':  # macOS and Linux
                os.system(f'open "{file_path}"' if os.uname().sysname == 'Darwin' else f'xdg-open "{file_path}"')
            
            return SkillResult(
                success=True,
                message=f"Opening {results[0].name}",
                data={'opened_file': file_path},
                execution_time=0.0,
                skill_name=self.name
            )
            
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"I found the file but couldn't open it: {str(e)}",
                data={'file_path': file_path},
                execution_time=0.0,
                skill_name=self.name,
                error=str(e)
            )
    
    def _handle_file_list(self, context: SkillContext) -> SkillResult:
        """Handle listing files in a directory."""
        # Extract directory path
        directory = self._extract_directory_path(context.user_input)
        
        if not directory:
            directory = os.getcwd()  # Current directory
        
        try:
            if not os.path.exists(directory):
                return SkillResult(
                    success=False,
                    message=f"Directory '{directory}' does not exist.",
                    data={},
                    execution_time=0.0,
                    skill_name=self.name,
                    error="Directory not found"
                )
            
            # List files in directory
            files = []
            directories = []
            
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isfile(item_path):
                    files.append({
                        'name': item,
                        'path': item_path,
                        'type': 'file',
                        'size': os.path.getsize(item_path)
                    })
                elif os.path.isdir(item_path):
                    directories.append({
                        'name': item,
                        'path': item_path,
                        'type': 'directory'
                    })
            
            # Sort files by name
            files.sort(key=lambda x: x['name'].lower())
            directories.sort(key=lambda x: x['name'].lower())
            
            # Create response
            response = f"Files in {directory}:\n"
            
            if directories:
                response += "Directories:\n"
                for dir_info in directories[:10]:  # Limit to 10
                    response += f"  [DIR] {dir_info['name']}\n"
            
            if files:
                response += "Files:\n"
                for file_info in files[:10]:  # Limit to 10
                    size_str = self._format_file_size(file_info['size'])
                    response += f"  [FILE] {file_info['name']} ({size_str})\n"
            
            if len(files) + len(directories) > 20:
                response += f"... and {len(files) + len(directories) - 20} more items"
            
            return SkillResult(
                success=True,
                message=response,
                data={
                    'directory': directory,
                    'files': files,
                    'directories': directories
                },
                execution_time=0.0,
                skill_name=self.name
            )
            
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"I couldn't list files in '{directory}': {str(e)}",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error=str(e)
            )
    
    def _extract_search_query(self, user_input: str) -> Optional[str]:
        """Extract search query from user input."""
        import re
        
        # Clean up input first (remove leading punctuation)
        user_input = user_input.strip().lstrip(',').strip()
        user_input_lower = user_input.lower()
        
        # Pattern 1: "find files with 'X' in the name"
        match = re.search(r"with\s+['\"]?([^'\"]+)['\"]?\s+in\s+the\s+name", user_input_lower)
        if match:
            return match.group(1).strip()
        
        # Pattern 2: "search for X"
        match = re.search(r"search\s+for\s+(.+)", user_input_lower)
        if match:
            return match.group(1).strip()
        
        # Pattern 3: "find X"  
        match = re.search(r"find\s+(.+)", user_input_lower)
        if match:
            return match.group(1).strip()
        
        # Pattern 4: "locate X"
        match = re.search(r"locate\s+(.+)", user_input_lower)
        if match:
            return match.group(1).strip()
        
        # Remove common prefixes
        prefixes = [
            "search for", "find", "locate", "where is", "show me",
            "open file", "file named", "file called", "files"
        ]
        
        for prefix in prefixes:
            if user_input_lower.startswith(prefix):
                return user_input[len(prefix):].strip()
        
        # If no prefix found, return the whole input
        return user_input.strip()
    
    def _extract_directory_path(self, user_input: str) -> Optional[str]:
        """Extract directory path from user input."""
        user_input_lower = user_input.lower()
        
        # Look for directory indicators
        if "in " in user_input_lower:
            parts = user_input_lower.split("in ", 1)
            if len(parts) > 1:
                directory = parts[1].strip()
                # Handle special cases
                if directory in ["current directory", "current folder", "this directory", "this folder"]:
                    return os.getcwd()  # Return actual current directory
                return directory
        
        return None
    
    def _determine_search_type(self, user_input: str) -> str:
        """Determine the type of search to perform."""
        user_input_lower = user_input.lower()
        
        if any(keyword in user_input_lower for keyword in ["containing", "with content", "that contains"]):
            return "content"
        elif any(keyword in user_input_lower for keyword in ["document", "image", "video", "audio", "code"]):
            return "type"
        else:
            return "name"
    
    def _search_by_name(self, query: str) -> List:
        """Search files by name using graph search."""
        return self.fs_graph.search_by_name(query, max_results=20)
    
    def _search_by_content(self, query: str) -> List:
        """Search files by content."""
        # Determine file types to search
        file_types = None
        if any(ftype in query.lower() for ftype in self.file_type_mappings.keys()):
            for ftype, extensions in self.file_type_mappings.items():
                if ftype in query.lower():
                    file_types = extensions
                    break
        
        return self.fs_graph.search_by_content(query, file_types, max_results=20)
    
    def _search_by_type(self, query: str) -> List:
        """Search files by type."""
        file_types = []
        for ftype, extensions in self.file_type_mappings.items():
            if ftype in query.lower():
                file_types.extend(extensions)
        
        if not file_types:
            return []
        
        # Search for files with these extensions
        results = []
        for ext in file_types:
            ext_results = self.fs_graph.search_by_name(f"*{ext}", max_results=10)
            results.extend(ext_results)
        
        return results[:20]  # Limit total results
    
    def _format_file_size(self, size_bytes: int) -> str:
        """Format file size for display."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


class FileManagementSkill(BaseSkill):
    """
    Skill for file management operations like copy, move, delete.
    Demonstrates file system operations and error handling.
    """
    
    def __init__(self):
        super().__init__(
            name="file_management",
            description="Manage files with copy, move, delete operations",
            priority=SkillPriority.NORMAL
        )
        self.triggers = ["copy", "move", "delete", "rename", "create", "folder"]
    
    def can_handle(self, context: SkillContext) -> bool:
        """Check if this skill can handle file management."""
        user_input = context.user_input.lower()
        # More flexible management keywords
        management_keywords = [
            "copy", "move", "delete", "rename", "create", "folder", "directory",
            "duplicate", "remove", "trash", "new folder", "make folder",
            "file management", "organize files", "manage files", "file operations"
        ]
        return any(keyword in user_input for keyword in management_keywords)
    
    def execute(self, context: SkillContext) -> SkillResult:
        """Execute file management operation."""
        user_input = context.user_input.lower()
        
        try:
            if "copy" in user_input:
                return self._handle_copy(context)
            elif "move" in user_input:
                return self._handle_move(context)
            elif "delete" in user_input or "remove" in user_input:
                return self._handle_delete(context)
            elif "rename" in user_input:
                return self._handle_rename(context)
            elif "create" in user_input and ("folder" in user_input or "directory" in user_input):
                return self._handle_create_folder(context)
            else:
                return SkillResult(
                    success=False,
                    message="I didn't understand the file management operation you requested.",
                    data={},
                    execution_time=0.0,
                    skill_name=self.name,
                    error="Unknown operation"
                )
        
        except Exception as e:
            return SkillResult(
                success=False,
                message="Sorry, I had trouble with the file operation.",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error=str(e)
            )
    
    def _handle_copy(self, context: SkillContext) -> SkillResult:
        """Handle file copy operation."""
        # This is a simplified implementation
        # In a real system, you'd parse the source and destination paths
        return SkillResult(
            success=False,
            message="File copy operation not yet implemented. Please specify source and destination paths.",
            data={},
            execution_time=0.0,
            skill_name=self.name,
            error="Not implemented"
        )
    
    def _handle_move(self, context: SkillContext) -> SkillResult:
        """Handle file move operation."""
        return SkillResult(
            success=False,
            message="File move operation not yet implemented. Please specify source and destination paths.",
            data={},
            execution_time=0.0,
            skill_name=self.name,
            error="Not implemented"
        )
    
    def _handle_delete(self, context: SkillContext) -> SkillResult:
        """Handle file delete operation."""
        return SkillResult(
            success=False,
            message="File delete operation not yet implemented for safety reasons.",
            data={},
            execution_time=0.0,
            skill_name=self.name,
            error="Not implemented"
        )
    
    def _handle_rename(self, context: SkillContext) -> SkillResult:
        """Handle file rename operation."""
        return SkillResult(
            success=False,
            message="File rename operation not yet implemented. Please specify old and new names.",
            data={},
            execution_time=0.0,
            skill_name=self.name,
            error="Not implemented"
        )
    
    def _handle_create_folder(self, context: SkillContext) -> SkillResult:
        """Handle folder creation."""
        # Extract folder name from input
        user_input = context.user_input.lower()
        
        # Simple extraction - look for text after "create folder" or "create directory"
        if "create folder" in user_input:
            folder_name = user_input.split("create folder", 1)[1].strip()
        elif "create directory" in user_input:
            folder_name = user_input.split("create directory", 1)[1].strip()
        else:
            return SkillResult(
                success=False,
                message="Please specify the folder name to create.",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error="No folder name specified"
            )
        
        if not folder_name:
            return SkillResult(
                success=False,
                message="Please specify the folder name to create.",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error="Empty folder name"
            )
        
        try:
            # Create folder in current directory
            folder_path = os.path.join(os.getcwd(), folder_name)
            os.makedirs(folder_path, exist_ok=True)
            
            return SkillResult(
                success=True,
                message=f"Created folder '{folder_name}' in {os.getcwd()}",
                data={'folder_path': folder_path},
                execution_time=0.0,
                skill_name=self.name
            )
            
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Could not create folder '{folder_name}': {str(e)}",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error=str(e)
            )


if __name__ == "__main__":
    # Demo the file skills
    from voice_assistant.core.graph_search import FileSystemGraph
    
    # Create file system graph
    fs_graph = FileSystemGraph()
    
    # Create file search skill
    file_search_skill = FileSearchSkill(fs_graph)
    file_management_skill = FileManagementSkill()
    
    # Test file search
    context = SkillContext(
        user_input="Find files containing 'python'",
        intent="file_search",
        entities={},
        confidence=0.9,
        session_id="test"
    )
    
    result = file_search_skill.execute(context)
    print(f"File search result: {result.message}")
    
    # Test folder creation
    context2 = SkillContext(
        user_input="Create folder called 'test_folder'",
        intent="file_management",
        entities={},
        confidence=0.9,
        session_id="test"
    )
    
    result2 = file_management_skill.execute(context2)
    print(f"Folder creation result: {result2.message}")
