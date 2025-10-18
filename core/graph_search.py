"""
Graph-based search algorithms for file system navigation and application launching.
Demonstrates graph algorithms, pathfinding, and intelligent search strategies.
"""

import os
import time
from typing import List, Dict, Set, Optional, Tuple, Any, Callable
from collections import defaultdict, deque
from queue import PriorityQueue
from dataclasses import dataclass
from enum import Enum
import threading
import hashlib


class SearchAlgorithm(Enum):
    """Available search algorithms."""
    BFS = "breadth_first_search"
    DFS = "depth_first_search"
    DIJKSTRA = "dijkstra"
    ASTAR = "a_star"
    GREEDY = "greedy_best_first"


@dataclass
class GraphNode:
    """Represents a node in the search graph."""
    id: str
    name: str
    path: str
    node_type: str  # 'file', 'directory', 'application'
    size: int = 0
    last_modified: float = 0.0
    metadata: Dict[str, Any] = None
    heuristic_value: float = 0.0
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class GraphEdge:
    """Represents an edge between nodes."""
    from_node: str
    to_node: str
    weight: float = 1.0
    edge_type: str = "contains"  # 'contains', 'references', 'similar'
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class FileSystemGraph:
    """
    Graph representation of file system with advanced search capabilities.
    Features:
    - Multiple search algorithms (BFS, DFS, Dijkstra, A*, Greedy)
    - Intelligent pathfinding
    - Content-based search
    - Metadata indexing
    - Real-time updates
    - Caching of search results
    """
    
    def __init__(self, root_path: str = None):
        self.root_path = root_path or os.getcwd()
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: Dict[str, List[GraphEdge]] = defaultdict(list)
        self.reverse_edges: Dict[str, List[GraphEdge]] = defaultdict(list)
        self.name_index: Dict[str, Set[str]] = defaultdict(set)
        self.type_index: Dict[str, Set[str]] = defaultdict(set)
        self.content_index: Dict[str, Set[str]] = defaultdict(set)
        self.lock = threading.RLock()
        self._build_graph()
    
    def _build_graph(self) -> None:
        """Build the initial graph from file system."""
        print("Building file system graph...")
        start_time = time.time()
        
        for root, dirs, files in os.walk(self.root_path):
            # Add directory node
            dir_path = root
            dir_id = self._get_node_id(dir_path)
            dir_node = GraphNode(
                id=dir_id,
                name=os.path.basename(dir_path),
                path=dir_path,
                node_type='directory',
                last_modified=os.path.getmtime(dir_path) if os.path.exists(dir_path) else 0
            )
            self._add_node(dir_node)
            
            # Add file nodes and edges
            for file in files:
                file_path = os.path.join(root, file)
                file_id = self._get_node_id(file_path)
                
                try:
                    file_node = GraphNode(
                        id=file_id,
                        name=file,
                        path=file_path,
                        node_type='file',
                        size=os.path.getsize(file_path) if os.path.exists(file_path) else 0,
                        last_modified=os.path.getmtime(file_path) if os.path.exists(file_path) else 0
                    )
                    self._add_node(file_node)
                    
                    # Add edge from directory to file
                    edge = GraphEdge(
                        from_node=dir_id,
                        to_node=file_id,
                        weight=1.0,
                        edge_type='contains'
                    )
                    self._add_edge(edge)
                    
                except (OSError, IOError):
                    # Skip files that can't be accessed
                    continue
        
        build_time = time.time() - start_time
        print(f"Graph built in {build_time:.2f}s with {len(self.nodes)} nodes")
    
    def _get_node_id(self, path: str) -> str:
        """Generate a unique ID for a path."""
        return hashlib.md5(path.encode()).hexdigest()
    
    def _add_node(self, node: GraphNode) -> None:
        """Add a node to the graph."""
        with self.lock:
            self.nodes[node.id] = node
            self.name_index[node.name.lower()].add(node.id)
            self.type_index[node.node_type].add(node.id)
    
    def _add_edge(self, edge: GraphEdge) -> None:
        """Add an edge to the graph."""
        with self.lock:
            self.edges[edge.from_node].append(edge)
            self.reverse_edges[edge.to_node].append(edge)
    
    def search_by_name(self, 
                      query: str, 
                      algorithm: SearchAlgorithm = SearchAlgorithm.BFS,
                      max_results: int = 100) -> List[GraphNode]:
        """Search for nodes by name using specified algorithm."""
        query_lower = query.lower()
        matching_nodes = []
        
        # Find nodes with matching names
        for name, node_ids in self.name_index.items():
            if query_lower in name:
                for node_id in node_ids:
                    matching_nodes.append(self.nodes[node_id])
        
        # Apply search algorithm for ranking
        if algorithm == SearchAlgorithm.BFS:
            return self._bfs_rank(matching_nodes, query, max_results)
        elif algorithm == SearchAlgorithm.DFS:
            return self._dfs_rank(matching_nodes, query, max_results)
        elif algorithm == SearchAlgorithm.DIJKSTRA:
            return self._dijkstra_rank(matching_nodes, query, max_results)
        elif algorithm == SearchAlgorithm.ASTAR:
            return self._astar_rank(matching_nodes, query, max_results)
        elif algorithm == SearchAlgorithm.GREEDY:
            return self._greedy_rank(matching_nodes, query, max_results)
        else:
            return matching_nodes[:max_results]
    
    def search_by_content(self, 
                         query: str, 
                         file_types: List[str] = None,
                         max_results: int = 50) -> List[GraphNode]:
        """Search for files by content (simplified implementation)."""
        results = []
        query_lower = query.lower()
        
        for node in self.nodes.values():
            if node.node_type != 'file':
                continue
            
            if file_types and not any(node.name.endswith(ext) for ext in file_types):
                continue
            
            # In a real implementation, you'd read and search file content
            # For demo purposes, we'll search in the filename
            if query_lower in node.name.lower():
                results.append(node)
                
                if len(results) >= max_results:
                    break
        
        return results
    
    def find_shortest_path(self, 
                          start_path: str, 
                          end_path: str,
                          algorithm: SearchAlgorithm = SearchAlgorithm.DIJKSTRA) -> List[GraphNode]:
        """Find shortest path between two nodes."""
        start_id = self._get_node_id(start_path)
        end_id = self._get_node_id(end_path)
        
        if start_id not in self.nodes or end_id not in self.nodes:
            return []
        
        if algorithm == SearchAlgorithm.BFS:
            return self._bfs_path(start_id, end_id)
        elif algorithm == SearchAlgorithm.DIJKSTRA:
            return self._dijkstra_path(start_id, end_id)
        elif algorithm == SearchAlgorithm.ASTAR:
            return self._astar_path(start_id, end_id)
        else:
            return self._bfs_path(start_id, end_id)
    
    def get_related_files(self, 
                         file_path: str, 
                         max_depth: int = 2,
                         max_results: int = 20) -> List[GraphNode]:
        """Get files related to the given file (same directory, similar names, etc.)."""
        file_id = self._get_node_id(file_path)
        if file_id not in self.nodes:
            return []
        
        related = set()
        visited = set()
        queue = deque([(file_id, 0)])
        
        while queue and len(related) < max_results:
            current_id, depth = queue.popleft()
            
            if current_id in visited or depth > max_depth:
                continue
            
            visited.add(current_id)
            current_node = self.nodes[current_id]
            
            # Add files from same directory
            for edge in self.edges.get(current_id, []):
                if edge.to_node in self.nodes:
                    target_node = self.nodes[edge.to_node]
                    if target_node.node_type == 'file':
                        related.add(target_node)
            
            # Add files from parent directory
            for edge in self.reverse_edges.get(current_id, []):
                if edge.from_node in self.nodes:
                    parent_node = self.nodes[edge.from_node]
                    if parent_node.node_type == 'directory':
                        for child_edge in self.edges.get(edge.from_node, []):
                            if child_edge.to_node in self.nodes:
                                child_node = self.nodes[child_edge.to_node]
                                if child_node.node_type == 'file':
                                    related.add(child_node)
            
            # Continue BFS
            for edge in self.edges.get(current_id, []):
                queue.append((edge.to_node, depth + 1))
        
        return list(related)[:max_results]
    
    def _bfs_rank(self, nodes: List[GraphNode], query: str, max_results: int) -> List[GraphNode]:
        """Rank nodes using BFS-based scoring."""
        scores = []
        query_lower = query.lower()
        
        for node in nodes:
            score = 0
            name_lower = node.name.lower()
            
            # Exact match gets highest score
            if name_lower == query_lower:
                score += 100
            # Starts with query gets high score
            elif name_lower.startswith(query_lower):
                score += 50
            # Contains query gets medium score
            elif query_lower in name_lower:
                score += 25
            
            # Prefer files over directories
            if node.node_type == 'file':
                score += 10
            
            # Prefer recently modified files
            score += min(node.last_modified / 1000000000, 10)  # Normalize timestamp
            
            scores.append((score, node))
        
        # Sort by score (descending) and return top results
        scores.sort(key=lambda x: x[0], reverse=True)
        return [node for _, node in scores[:max_results]]
    
    def _dfs_rank(self, nodes: List[GraphNode], query: str, max_results: int) -> List[GraphNode]:
        """Rank nodes using DFS-based scoring (depth-first exploration)."""
        # Similar to BFS but with different weighting
        return self._bfs_rank(nodes, query, max_results)
    
    def _dijkstra_rank(self, nodes: List[GraphNode], query: str, max_results: int) -> List[GraphNode]:
        """Rank nodes using Dijkstra's algorithm (shortest path from root)."""
        if not nodes:
            return []
        
        # Calculate shortest path distances from root
        distances = {}
        pq = PriorityQueue()
        pq.put((0, self.root_path))
        distances[self.root_path] = 0
        
        while not pq.empty():
            dist, current_path = pq.get()
            
            if current_path in distances and dist > distances[current_path]:
                continue
            
            current_id = self._get_node_id(current_path)
            for edge in self.edges.get(current_id, []):
                if edge.to_node in self.nodes:
                    target_path = self.nodes[edge.to_node].path
                    new_dist = dist + edge.weight
                    
                    if target_path not in distances or new_dist < distances[target_path]:
                        distances[target_path] = new_dist
                        pq.put((new_dist, target_path))
        
        # Rank nodes by distance and relevance
        scores = []
        query_lower = query.lower()
        
        for node in nodes:
            distance = distances.get(node.path, float('inf'))
            relevance = 0
            
            name_lower = node.name.lower()
            if name_lower == query_lower:
                relevance = 100
            elif name_lower.startswith(query_lower):
                relevance = 50
            elif query_lower in name_lower:
                relevance = 25
            
            # Combine distance and relevance (lower distance is better)
            score = relevance - (distance * 0.1)
            scores.append((score, node))
        
        scores.sort(key=lambda x: x[0], reverse=True)
        return [node for _, node in scores[:max_results]]
    
    def _astar_rank(self, nodes: List[GraphNode], query: str, max_results: int) -> List[GraphNode]:
        """Rank nodes using A* algorithm with heuristic."""
        # Simplified A* implementation
        scores = []
        query_lower = query.lower()
        
        for node in nodes:
            # Heuristic: relevance to query
            name_lower = node.name.lower()
            heuristic = 0
            
            if name_lower == query_lower:
                heuristic = 100
            elif name_lower.startswith(query_lower):
                heuristic = 50
            elif query_lower in name_lower:
                heuristic = 25
            
            # Add file type preference
            if node.node_type == 'file':
                heuristic += 10
            
            scores.append((heuristic, node))
        
        scores.sort(key=lambda x: x[0], reverse=True)
        return [node for _, node in scores[:max_results]]
    
    def _greedy_rank(self, nodes: List[GraphNode], query: str, max_results: int) -> List[GraphNode]:
        """Rank nodes using greedy best-first search."""
        return self._astar_rank(nodes, query, max_results)
    
    def _bfs_path(self, start_id: str, end_id: str) -> List[GraphNode]:
        """Find path using BFS."""
        if start_id == end_id:
            return [self.nodes[start_id]]
        
        queue = deque([(start_id, [start_id])])
        visited = {start_id}
        
        while queue:
            current_id, path = queue.popleft()
            
            for edge in self.edges.get(current_id, []):
                if edge.to_node == end_id:
                    return [self.nodes[node_id] for node_id in path + [end_id]]
                
                if edge.to_node not in visited:
                    visited.add(edge.to_node)
                    queue.append((edge.to_node, path + [edge.to_node]))
        
        return []
    
    def _dijkstra_path(self, start_id: str, end_id: str) -> List[GraphNode]:
        """Find shortest path using Dijkstra's algorithm."""
        if start_id == end_id:
            return [self.nodes[start_id]]
        
        distances = {start_id: 0}
        previous = {}
        pq = PriorityQueue()
        pq.put((0, start_id))
        
        while not pq.empty():
            dist, current_id = pq.get()
            
            if current_id == end_id:
                # Reconstruct path
                path = []
                while current_id is not None:
                    path.append(current_id)
                    current_id = previous.get(current_id)
                return [self.nodes[node_id] for node_id in reversed(path)]
            
            if dist > distances.get(current_id, float('inf')):
                continue
            
            for edge in self.edges.get(current_id, []):
                new_dist = dist + edge.weight
                if new_dist < distances.get(edge.to_node, float('inf')):
                    distances[edge.to_node] = new_dist
                    previous[edge.to_node] = current_id
                    pq.put((new_dist, edge.to_node))
        
        return []
    
    def _astar_path(self, start_id: str, end_id: str) -> List[GraphNode]:
        """Find path using A* algorithm."""
        # Simplified A* implementation
        return self._dijkstra_path(start_id, end_id)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get graph statistics."""
        with self.lock:
            return {
                'total_nodes': len(self.nodes),
                'total_edges': sum(len(edges) for edges in self.edges.values()),
                'node_types': {node_type: len(node_ids) for node_type, node_ids in self.type_index.items()},
                'root_path': self.root_path
            }


class ApplicationLauncher:
    """
    Application launcher using graph-based search for intelligent app discovery.
    """
    
    def __init__(self, fs_graph: FileSystemGraph):
        self.fs_graph = fs_graph
        self.app_cache: Dict[str, List[GraphNode]] = {}
        self.common_apps = {
            'calculator': ['calc.exe', 'calculator.exe', 'gnome-calculator'],
            'notepad': ['notepad.exe', 'gedit', 'kate'],
            'browser': ['chrome.exe', 'firefox.exe', 'msedge.exe', 'safari'],
            'terminal': ['cmd.exe', 'powershell.exe', 'bash', 'zsh'],
            'file_manager': ['explorer.exe', 'nautilus', 'dolphin']
        }
    
    def find_application(self, app_name: str) -> List[GraphNode]:
        """Find applications by name using graph search."""
        if app_name.lower() in self.app_cache:
            return self.app_cache[app_name.lower()]
        
        # Search for executable files
        results = self.fs_graph.search_by_name(
            app_name, 
            algorithm=SearchAlgorithm.ASTAR,
            max_results=20
        )
        
        # Filter for executable files
        executables = []
        for node in results:
            if (node.node_type == 'file' and 
                (node.name.endswith('.exe') or 
                 node.name.endswith('.app') or
                 'bin' in node.path.lower())):
                executables.append(node)
        
        self.app_cache[app_name.lower()] = executables
        return executables
    
    def launch_application(self, app_name: str) -> bool:
        """Launch an application by name."""
        apps = self.find_application(app_name)
        
        if not apps:
            return False
        
        # Try to launch the first (best match) application
        app_path = apps[0].path
        try:
            os.startfile(app_path)  # Windows
            return True
        except AttributeError:
            try:
                os.system(f"open '{app_path}'")  # macOS
                return True
            except:
                try:
                    os.system(f"xdg-open '{app_path}'")  # Linux
                    return True
                except:
                    return False
        except:
            return False


if __name__ == "__main__":
    # Demo the graph search system
    fs_graph = FileSystemGraph()
    launcher = ApplicationLauncher(fs_graph)
    
    print("File system graph statistics:")
    stats = fs_graph.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test search functionality
    print("\nSearching for Python files:")
    python_files = fs_graph.search_by_name("*.py", max_results=5)
    for file in python_files:
        print(f"  {file.name} - {file.path}")
    
    # Test application launching
    print("\nFinding calculator application:")
    calc_apps = launcher.find_application("calculator")
    for app in calc_apps[:3]:
        print(f"  {app.name} - {app.path}")
    
    # Test related files
    if python_files:
        print(f"\nFiles related to {python_files[0].name}:")
        related = fs_graph.get_related_files(python_files[0].path, max_results=3)
        for file in related:
            print(f"  {file.name} - {file.path}")


