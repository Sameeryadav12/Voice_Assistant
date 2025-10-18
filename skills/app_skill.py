"""
Application launcher skill using graph-based search and system integration.
Demonstrates application discovery, launching, and system control.
"""

import os
import subprocess
import psutil
from typing import Dict, List, Any, Optional
from skills.base_skill import BaseSkill, SkillContext, SkillResult, SkillPriority
from core.graph_search import ApplicationLauncher


class AppLauncherSkill(BaseSkill):
    """
    Skill for launching applications using intelligent search algorithms.
    Demonstrates integration with graph-based search and system operations.
    """
    
    def __init__(self, fs_graph):
        super().__init__(
            name="app_launcher",
            description="Launch applications using intelligent search",
            priority=SkillPriority.HIGH
        )
        self.fs_graph = fs_graph
        self.app_launcher = ApplicationLauncher(fs_graph)
        self.triggers = ["open", "launch", "start", "run", "app", "application", "program"]
        self.required_entities = []
        self.optional_entities = ["app_name", "app_type"]
        
        # Common application mappings
        self.app_mappings = {
            'calculator': ['calc', 'calculator', 'calc.exe'],
            'notepad': ['notepad', 'notepad.exe', 'text editor'],
            'chrome': ['chrome', 'google chrome', 'browser'],
            'edge': ['edge', 'microsoft edge'],
            'firefox': ['firefox', 'mozilla'],
            'cmd': ['cmd', 'command prompt', 'command', 'terminal'],
            'powershell': ['powershell', 'pwsh'],
            'explorer': ['explorer', 'file manager', 'file explorer', 'files'],
            'text editor': ['notepad', 'vscode', 'sublime', 'atom', 'editor'],
            'media player': ['vlc', 'media player', 'player', 'music'],
            'image viewer': ['photos', 'image viewer', 'viewer', 'gallery'],
            'pdf reader': ['adobe', 'pdf reader', 'reader', 'acrobat'],
            'office': ['word', 'excel', 'powerpoint', 'office', 'microsoft']
        }
        
        # System-specific application paths
        self.system_apps = self._get_system_applications()
    
    def _get_system_applications(self) -> Dict[str, str]:
        """Get system-specific application paths."""
        system_apps = {}
        
        if os.name == 'nt':  # Windows
            system_apps = {
                'calculator': 'calc.exe',
                'notepad': 'notepad.exe',
                'command prompt': 'cmd.exe',
                'cmd': 'cmd.exe',
                'powershell': 'powershell.exe',
                'file explorer': 'explorer.exe',
                'explorer': 'explorer.exe',
                'task manager': 'taskmgr.exe',
                'control panel': 'control.exe',
                'device manager': 'devmgmt.msc',
                'registry editor': 'regedit.exe',
                'system information': 'msinfo32.exe',
                'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                'google chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                'edge': 'msedge.exe',
                'microsoft edge': 'msedge.exe',
                'firefox': r'C:\Program Files\Mozilla Firefox\firefox.exe',
                'paint': 'mspaint.exe',
                'wordpad': 'write.exe'
            }
        elif os.name == 'posix':  # macOS and Linux
            if os.uname().sysname == 'Darwin':  # macOS
                system_apps = {
                    'calculator': '/Applications/Calculator.app',
                    'textedit': '/Applications/TextEdit.app',
                    'terminal': '/Applications/Utilities/Terminal.app',
                    'finder': '/System/Library/CoreServices/Finder.app',
                    'safari': '/Applications/Safari.app',
                    'mail': '/Applications/Mail.app',
                    'calendar': '/Applications/Calendar.app'
                }
            else:  # Linux
                system_apps = {
                    'calculator': 'gnome-calculator',
                    'text editor': 'gedit',
                    'terminal': 'gnome-terminal',
                    'file manager': 'nautilus',
                    'browser': 'firefox'
                }
        
        return system_apps
    
    def can_handle(self, context: SkillContext) -> bool:
        """Check if this skill can handle app launching."""
        user_input = context.user_input.lower()
        
        launch_keywords = ["open", "launch", "start", "run", "app", "application", "program"]
        return any(keyword in user_input for keyword in launch_keywords)
    
    def execute(self, context: SkillContext) -> SkillResult:
        """Execute application launching."""
        try:
            user_input = context.user_input.lower()
            
            # Determine operation type
            if any(keyword in user_input for keyword in ["list", "show", "what apps", "available"]):
                return self._handle_list_apps(context)
            elif any(keyword in user_input for keyword in ["close", "quit", "exit", "stop"]):
                return self._handle_close_app(context)
            elif any(keyword in user_input for keyword in ["running", "active", "current"]):
                return self._handle_list_running_apps(context)
            else:
                return self._handle_launch_app(context)
        
        except Exception as e:
            return SkillResult(
                success=False,
                message="Sorry, I had trouble with the application operation.",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error=str(e)
            )
    
    def _handle_launch_app(self, context: SkillContext) -> SkillResult:
        """Handle launching an application."""
        # Extract application name
        app_name = self._extract_app_name(context.user_input)
        
        if not app_name:
            return SkillResult(
                success=False,
                message="What application would you like me to open?",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error="No app name specified"
            )
        
        # Try to launch the application
        success, message, app_path = self._launch_application(app_name)
        
        if success:
            return SkillResult(
                success=True,
                message=message,
                data={'app_name': app_name, 'app_path': app_path},
                execution_time=0.0,
                skill_name=self.name
            )
        else:
            return SkillResult(
                success=False,
                message=message,
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error="Launch failed"
            )
    
    def _handle_list_apps(self, context: SkillContext) -> SkillResult:
        """Handle listing available applications."""
        try:
            # Get system applications
            system_apps = list(self.system_apps.keys())
            
            # Get discovered applications from graph
            discovered_apps = []
            for app_name in self.app_mappings.keys():
                apps = self.app_launcher.find_application(app_name)
                if apps:
                    discovered_apps.extend([app.name for app in apps[:3]])  # Top 3 per category
            
            # Combine and format
            all_apps = system_apps + discovered_apps
            all_apps = list(set(all_apps))  # Remove duplicates
            all_apps.sort()
            
            if not all_apps:
                return SkillResult(
                    success=True,
                    message="I couldn't find any applications to list.",
                    data={'apps': []},
                    execution_time=0.0,
                    skill_name=self.name
                )
            
            # Create response
            response = "Here are some applications I can launch:\n"
            for i, app in enumerate(all_apps[:15]):  # Limit to 15 apps
                response += f"{i+1}. {app}\n"
            
            if len(all_apps) > 15:
                response += f"... and {len(all_apps) - 15} more applications"
            
            return SkillResult(
                success=True,
                message=response,
                data={'apps': all_apps},
                execution_time=0.0,
                skill_name=self.name
            )
            
        except Exception as e:
            return SkillResult(
                success=False,
                message="Sorry, I couldn't list the applications.",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error=str(e)
            )
    
    def _handle_close_app(self, context: SkillContext) -> SkillResult:
        """Handle closing an application."""
        app_name = self._extract_app_name(context.user_input)
        
        if not app_name:
            return SkillResult(
                success=False,
                message="What application would you like me to close?",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error="No app name specified"
            )
        
        # Find running processes
        running_processes = self._get_running_processes()
        matching_processes = []
        
        for process in running_processes:
            if app_name.lower() in process['name'].lower():
                matching_processes.append(process)
        
        if not matching_processes:
            return SkillResult(
                success=False,
                message=f"I couldn't find any running applications matching '{app_name}'.",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error="App not found"
            )
        
        # Close the first matching process
        try:
            process = psutil.Process(matching_processes[0]['pid'])
            process.terminate()
            
            return SkillResult(
                success=True,
                message=f"Closed {matching_processes[0]['name']}",
                data={'closed_app': matching_processes[0]['name']},
                execution_time=0.0,
                skill_name=self.name
            )
            
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"I found the application but couldn't close it: {str(e)}",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error=str(e)
            )
    
    def _handle_list_running_apps(self, context: SkillContext) -> SkillResult:
        """Handle listing running applications."""
        try:
            running_processes = self._get_running_processes()
            
            if not running_processes:
                return SkillResult(
                    success=True,
                    message="No applications are currently running.",
                    data={'running_apps': []},
                    execution_time=0.0,
                    skill_name=self.name
                )
            
            # Format response
            response = "Currently running applications:\n"
            for i, process in enumerate(running_processes[:10]):  # Limit to 10
                response += f"{i+1}. {process['name']} (PID: {process['pid']})\n"
            
            if len(running_processes) > 10:
                response += f"... and {len(running_processes) - 10} more processes"
            
            return SkillResult(
                success=True,
                message=response,
                data={'running_apps': running_processes},
                execution_time=0.0,
                skill_name=self.name
            )
            
        except Exception as e:
            return SkillResult(
                success=False,
                message="Sorry, I couldn't list the running applications.",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error=str(e)
            )
    
    def _extract_app_name(self, user_input: str) -> Optional[str]:
        """Extract application name from user input."""
        user_input_lower = user_input.lower()
        
        # Remove common prefixes
        prefixes = ["open", "launch", "start", "run", "close", "quit", "exit"]
        for prefix in prefixes:
            if user_input_lower.startswith(prefix):
                return user_input[len(prefix):].strip()
        
        # Look for app keywords
        app_keywords = ["app", "application", "program"]
        for keyword in app_keywords:
            if keyword in user_input_lower:
                # Extract text around the keyword
                parts = user_input_lower.split(keyword)
                if len(parts) > 1:
                    return parts[1].strip()
        
        return user_input.strip()
    
    def _launch_application(self, app_name: str) -> tuple[bool, str, Optional[str]]:
        """Launch an application and return success status, message, and path."""
        app_name_lower = app_name.lower()
        
        # Special handling for Chrome (multiple possible paths)
        if 'chrome' in app_name_lower:
            chrome_paths = [
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
                os.path.expanduser(r'~\AppData\Local\Google\Chrome\Application\chrome.exe')
            ]
            for chrome_path in chrome_paths:
                if os.path.exists(chrome_path):
                    try:
                        subprocess.Popen([chrome_path])
                        return True, "Opened Google Chrome", chrome_path
                    except Exception as e:
                        continue
            # If not found in standard paths, try start command
            try:
                subprocess.Popen(['start', 'chrome'], shell=True)
                return True, "Opened Google Chrome", "chrome"
            except:
                pass
        
        # Check system applications first
        for sys_app, path in self.system_apps.items():
            if app_name_lower in sys_app.lower() or sys_app.lower() in app_name_lower:
                try:
                    if os.name == 'nt':  # Windows
                        # Special handling for cmd - needs different approach
                        if 'cmd' in path.lower():
                            subprocess.Popen(['start', 'cmd'], shell=True)
                        else:
                            subprocess.Popen([path], shell=True)
                    else:  # macOS and Linux
                        subprocess.Popen([path])
                    
                    return True, f"Opened {sys_app}", path
                except Exception as e:
                    print(f"Error launching {sys_app}: {e}")
                    continue
        
        # Check app mappings
        for category, apps in self.app_mappings.items():
            if app_name_lower in category.lower() or any(app in app_name_lower for app in apps):
                # Use graph search to find the application
                found_apps = self.app_launcher.find_application(category)
                if found_apps:
                    app_path = found_apps[0].path
                    try:
                        if self.app_launcher.launch_application(category):
                            return True, f"Opened {found_apps[0].name}", app_path
                    except Exception as e:
                        continue
        
        # Try direct graph search
        found_apps = self.app_launcher.find_application(app_name)
        if found_apps:
            app_path = found_apps[0].path
            try:
                if self.app_launcher.launch_application(app_name):
                    return True, f"Opened {found_apps[0].name}", app_path
            except Exception as e:
                pass
        
        return False, f"I couldn't find or launch an application matching '{app_name}'", None
    
    def _get_running_processes(self) -> List[Dict[str, Any]]:
        """Get list of running processes."""
        processes = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    proc_info = proc.info
                    # Filter out system processes and very low resource usage
                    if (proc_info['cpu_percent'] > 0.1 or proc_info['memory_percent'] > 0.1):
                        processes.append({
                            'pid': proc_info['pid'],
                            'name': proc_info['name'],
                            'cpu_percent': proc_info['cpu_percent'],
                            'memory_percent': proc_info['memory_percent']
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            print(f"Error getting running processes: {e}")
        
        # Sort by CPU usage (descending)
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        
        return processes


class SystemControlSkill(BaseSkill):
    """
    Skill for system control operations like shutdown, restart, sleep.
    Demonstrates system integration and safety measures.
    """
    
    def __init__(self):
        super().__init__(
            name="system_control",
            description="Control system operations like shutdown and restart",
            priority=SkillPriority.CRITICAL
        )
        self.triggers = ["shutdown", "restart", "sleep", "lock", "logout", "hibernate"]
        self.required_entities = []
        self.optional_entities = ["delay", "time"]
    
    def can_handle(self, context: SkillContext) -> bool:
        """Check if this skill can handle system control."""
        user_input = context.user_input.lower()
        system_keywords = ["shutdown", "restart", "sleep", "lock", "logout", "hibernate", "power"]
        return any(keyword in user_input for keyword in system_keywords)
    
    def execute(self, context: SkillContext) -> SkillResult:
        """Execute system control operation."""
        user_input = context.user_input.lower()
        
        try:
            if "shutdown" in user_input or "power off" in user_input:
                return self._handle_shutdown(context)
            elif "restart" in user_input or "reboot" in user_input:
                return self._handle_restart(context)
            elif "sleep" in user_input or "suspend" in user_input:
                return self._handle_sleep(context)
            elif "lock" in user_input:
                return self._handle_lock(context)
            elif "logout" in user_input or "sign out" in user_input:
                return self._handle_logout(context)
            elif "hibernate" in user_input:
                return self._handle_hibernate(context)
            else:
                return SkillResult(
                    success=False,
                    message="I didn't understand the system control operation you requested.",
                    data={},
                    execution_time=0.0,
                    skill_name=self.name,
                    error="Unknown operation"
                )
        
        except Exception as e:
            return SkillResult(
                success=False,
                message="Sorry, I had trouble with the system operation.",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error=str(e)
            )
    
    def _handle_shutdown(self, context: SkillContext) -> SkillResult:
        """Handle system shutdown."""
        # For safety, we'll just return a message instead of actually shutting down
        return SkillResult(
            success=True,
            message="I understand you want to shutdown the system, but for safety reasons, I cannot perform this operation automatically. Please use the system menu or press Alt+F4.",
            data={'operation': 'shutdown'},
            execution_time=0.0,
            skill_name=self.name
        )
    
    def _handle_restart(self, context: SkillContext) -> SkillResult:
        """Handle system restart."""
        return SkillResult(
            success=True,
            message="I understand you want to restart the system, but for safety reasons, I cannot perform this operation automatically. Please use the system menu.",
            data={'operation': 'restart'},
            execution_time=0.0,
            skill_name=self.name
        )
    
    def _handle_sleep(self, context: SkillContext) -> SkillResult:
        """Handle system sleep."""
        try:
            if os.name == 'nt':  # Windows
                os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
            elif os.name == 'posix':  # macOS and Linux
                os.system('pmset sleepnow' if os.uname().sysname == 'Darwin' else 'systemctl suspend')
            
            return SkillResult(
                success=True,
                message="Putting the system to sleep...",
                data={'operation': 'sleep'},
                execution_time=0.0,
                skill_name=self.name
            )
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Could not put system to sleep: {str(e)}",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error=str(e)
            )
    
    def _handle_lock(self, context: SkillContext) -> SkillResult:
        """Handle screen lock."""
        try:
            if os.name == 'nt':  # Windows
                os.system('rundll32.exe user32.dll,LockWorkStation')
            elif os.name == 'posix':  # macOS and Linux
                os.system('pmset displaysleepnow' if os.uname().sysname == 'Darwin' else 'gnome-screensaver-command -l')
            
            return SkillResult(
                success=True,
                message="Locking the screen...",
                data={'operation': 'lock'},
                execution_time=0.0,
                skill_name=self.name
            )
        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Could not lock screen: {str(e)}",
                data={},
                execution_time=0.0,
                skill_name=self.name,
                error=str(e)
            )
    
    def _handle_logout(self, context: SkillContext) -> SkillResult:
        """Handle user logout."""
        return SkillResult(
            success=True,
            message="I understand you want to logout, but for safety reasons, I cannot perform this operation automatically. Please use the system menu.",
            data={'operation': 'logout'},
            execution_time=0.0,
            skill_name=self.name
        )
    
    def _handle_hibernate(self, context: SkillContext) -> SkillResult:
        """Handle system hibernate."""
        return SkillResult(
            success=True,
            message="I understand you want to hibernate the system, but for safety reasons, I cannot perform this operation automatically. Please use the system menu.",
            data={'operation': 'hibernate'},
            execution_time=0.0,
            skill_name=self.name
        )


if __name__ == "__main__":
    # Demo the app skills
    from voice_assistant.core.graph_search import FileSystemGraph
    
    # Create file system graph
    fs_graph = FileSystemGraph()
    
    # Create app launcher skill
    app_skill = AppLauncherSkill(fs_graph)
    system_skill = SystemControlSkill()
    
    # Test app launching
    context = SkillContext(
        user_input="Open calculator",
        intent="app_launch",
        entities={},
        confidence=0.9,
        session_id="test"
    )
    
    result = app_skill.execute(context)
    print(f"App launch result: {result.message}")
    
    # Test system control
    context2 = SkillContext(
        user_input="Lock the screen",
        intent="system_control",
        entities={},
        confidence=0.9,
        session_id="test"
    )
    
    result2 = system_skill.execute(context2)
    print(f"System control result: {result2.message}")
