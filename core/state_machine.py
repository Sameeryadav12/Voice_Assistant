"""
Finite State Machine implementation for dialogue management and conversation flow.
Demonstrates state pattern, transition management, and event-driven architecture.
"""

from typing import Dict, List, Optional, Callable, Any, Set, Tuple
from enum import Enum
from dataclasses import dataclass
from collections import defaultdict, deque
import time
import threading


class StateType(Enum):
    """Types of states in the dialogue state machine."""
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"
    RESPONDING = "responding"
    WAITING_FOR_CONFIRMATION = "waiting_for_confirmation"
    ERROR = "error"
    SLEEP = "sleep"


class EventType(Enum):
    """Types of events that can trigger state transitions."""
    WAKE_WORD_DETECTED = "wake_word_detected"
    SPEECH_RECOGNIZED = "speech_recognized"
    INTENT_CLASSIFIED = "intent_classified"
    RESPONSE_READY = "response_ready"
    CONFIRMATION_RECEIVED = "confirmation_received"
    TIMEOUT = "timeout"
    ERROR_OCCURRED = "error_occurred"
    SLEEP_COMMAND = "sleep_command"
    WAKE_UP = "wake_up"


@dataclass
class StateTransition:
    """Represents a transition between states."""
    from_state: StateType
    to_state: StateType
    event: EventType
    condition: Optional[Callable[[Dict], bool]] = None
    action: Optional[Callable[[Dict], None]] = None
    priority: int = 0


@dataclass
class StateContext:
    """Context data passed between states."""
    user_input: str = ""
    recognized_text: str = ""
    intent: str = ""
    entities: Dict[str, Any] = None
    response: str = ""
    confidence: float = 0.0
    error_message: str = ""
    timestamp: float = 0.0
    retry_count: int = 0
    
    def __post_init__(self):
        if self.entities is None:
            self.entities = {}
        if self.timestamp == 0.0:
            self.timestamp = time.time()


class DialogueStateMachine:
    """
    Advanced finite state machine for managing dialogue flow.
    Features:
    - Hierarchical state management
    - Event-driven transitions
    - Timeout handling
    - Error recovery
    - State history tracking
    - Concurrent state handling
    """
    
    def __init__(self):
        self.current_state = StateType.IDLE
        self.previous_state = None
        self.state_history = deque(maxlen=100)  # Circular buffer for state history
        self.transitions: Dict[StateType, List[StateTransition]] = defaultdict(list)
        self.state_handlers: Dict[StateType, Callable] = {}
        self.context = StateContext()
        self.timeout_handlers: Dict[StateType, float] = {}
        self.lock = threading.RLock()
        self._setup_default_transitions()
        self._setup_state_handlers()
    
    def _setup_default_transitions(self) -> None:
        """Setup default state transitions for the dialogue flow."""
        transitions = [
            # Wake word detection
            StateTransition(StateType.IDLE, StateType.LISTENING, EventType.WAKE_WORD_DETECTED),
            StateTransition(StateType.SLEEP, StateType.LISTENING, EventType.WAKE_WORD_DETECTED),
            
            # Speech processing
            StateTransition(StateType.LISTENING, StateType.PROCESSING, EventType.SPEECH_RECOGNIZED),
            StateTransition(StateType.PROCESSING, StateType.RESPONDING, EventType.INTENT_CLASSIFIED),
            StateTransition(StateType.PROCESSING, StateType.ERROR, EventType.ERROR_OCCURRED),
            
            # Response handling
            StateTransition(StateType.RESPONDING, StateType.IDLE, EventType.RESPONSE_READY),
            StateTransition(StateType.RESPONDING, StateType.WAITING_FOR_CONFIRMATION, 
                          EventType.RESPONSE_READY, 
                          condition=lambda ctx: ctx.confidence < 0.8),
            
            # Confirmation handling
            StateTransition(StateType.WAITING_FOR_CONFIRMATION, StateType.IDLE, 
                          EventType.CONFIRMATION_RECEIVED),
            StateTransition(StateType.WAITING_FOR_CONFIRMATION, StateType.PROCESSING, 
                          EventType.SPEECH_RECOGNIZED),
            
            # Error handling
            StateTransition(StateType.ERROR, StateType.IDLE, EventType.TIMEOUT),
            StateTransition(StateType.ERROR, StateType.LISTENING, EventType.WAKE_WORD_DETECTED),
            
            # Sleep/wake
            StateTransition(StateType.IDLE, StateType.SLEEP, EventType.SLEEP_COMMAND),
            StateTransition(StateType.SLEEP, StateType.IDLE, EventType.WAKE_UP),
            
            # Timeout handling
            StateTransition(StateType.LISTENING, StateType.IDLE, EventType.TIMEOUT),
            StateTransition(StateType.PROCESSING, StateType.IDLE, EventType.TIMEOUT),
            StateTransition(StateType.WAITING_FOR_CONFIRMATION, StateType.IDLE, EventType.TIMEOUT),
        ]
        
        for transition in transitions:
            self.add_transition(transition)
    
    def _setup_state_handlers(self) -> None:
        """Setup handlers for each state."""
        self.state_handlers = {
            StateType.IDLE: self._handle_idle,
            StateType.LISTENING: self._handle_listening,
            StateType.PROCESSING: self._handle_processing,
            StateType.RESPONDING: self._handle_responding,
            StateType.WAITING_FOR_CONFIRMATION: self._handle_waiting_for_confirmation,
            StateType.ERROR: self._handle_error,
            StateType.SLEEP: self._handle_sleep,
        }
    
    def add_transition(self, transition: StateTransition) -> None:
        """Add a new state transition."""
        with self.lock:
            self.transitions[transition.from_state].append(transition)
            # Sort by priority (higher priority first)
            self.transitions[transition.from_state].sort(key=lambda t: t.priority, reverse=True)
    
    def process_event(self, event: EventType, context_data: Dict = None) -> bool:
        """
        Process an event and potentially transition to a new state.
        Returns True if transition occurred, False otherwise.
        """
        with self.lock:
            if context_data:
                self._update_context(context_data)
            
            # Find applicable transitions
            applicable_transitions = self._find_applicable_transitions(event)
            
            if not applicable_transitions:
                return False
            
            # Execute the highest priority transition
            transition = applicable_transitions[0]
            return self._execute_transition(transition)
    
    def _find_applicable_transitions(self, event: EventType) -> List[StateTransition]:
        """Find all transitions applicable for the current state and event."""
        applicable = []
        
        for transition in self.transitions[self.current_state]:
            if transition.event == event:
                # Check condition if present
                if transition.condition is None or transition.condition(self.context):
                    applicable.append(transition)
        
        return applicable
    
    def _execute_transition(self, transition: StateTransition) -> bool:
        """Execute a state transition."""
        # Execute exit action for current state
        if hasattr(self, f'_exit_{self.current_state.value}'):
            getattr(self, f'_exit_{self.current_state.value}')(self.context)
        
        # Update state
        self.previous_state = self.current_state
        self.current_state = transition.to_state
        
        # Record state change
        self.state_history.append({
            'from': self.previous_state,
            'to': self.current_state,
            'event': transition.event,
            'timestamp': time.time(),
            'context': self.context.__dict__.copy()
        })
        
        # Execute transition action
        if transition.action:
            transition.action(self.context)
        
        # Execute entry action for new state
        if hasattr(self, f'_enter_{self.current_state.value}'):
            getattr(self, f'_enter_{self.current_state.value}')(self.context)
        
        # Execute state handler
        if self.current_state in self.state_handlers:
            self.state_handlers[self.current_state](self.context)
        
        return True
    
    def _update_context(self, data: Dict) -> None:
        """Update the state context with new data."""
        for key, value in data.items():
            if hasattr(self.context, key):
                setattr(self.context, key, value)
    
    # State handlers
    def _handle_idle(self, context: StateContext) -> None:
        """Handle idle state - waiting for wake word."""
        context.retry_count = 0
        context.error_message = ""
    
    def _handle_listening(self, context: StateContext) -> None:
        """Handle listening state - capturing audio."""
        context.recognized_text = ""
        context.confidence = 0.0
    
    def _handle_processing(self, context: StateContext) -> None:
        """Handle processing state - analyzing speech."""
        context.intent = ""
        context.entities = {}
    
    def _handle_responding(self, context: StateContext) -> None:
        """Handle responding state - generating response."""
        pass  # Response generation handled by other components
    
    def _handle_waiting_for_confirmation(self, context: StateContext) -> None:
        """Handle waiting for confirmation state."""
        pass  # Confirmation handling logic
    
    def _handle_error(self, context: StateContext) -> None:
        """Handle error state - managing errors and recovery."""
        context.retry_count += 1
    
    def _handle_sleep(self, context: StateContext) -> None:
        """Handle sleep state - low power mode."""
        pass
    
    # State entry/exit handlers
    def _enter_listening(self, context: StateContext) -> None:
        """Entry handler for listening state."""
        print("[MIC] Listening for speech...")
    
    def _enter_processing(self, context: StateContext) -> None:
        """Entry handler for processing state."""
        print("[BRAIN] Processing speech...")
    
    def _enter_responding(self, context: StateContext) -> None:
        """Entry handler for responding state."""
        print("[SPEAK] Generating response...")
    
    def _enter_error(self, context: StateContext) -> None:
        """Entry handler for error state."""
        print(f"[ERROR] Error: {context.error_message}")
    
    def _enter_sleep(self, context: StateContext) -> None:
        """Entry handler for sleep state."""
        print("[SLEEP] Entering sleep mode...")
    
    def get_state_info(self) -> Dict:
        """Get current state information."""
        with self.lock:
            return {
                'current_state': self.current_state.value,
                'previous_state': self.previous_state.value if self.previous_state else None,
                'context': self.context.__dict__.copy(),
                'state_history_length': len(self.state_history),
                'available_transitions': len(self.transitions[self.current_state])
            }
    
    def get_state_history(self, limit: int = 10) -> List[Dict]:
        """Get recent state history."""
        with self.lock:
            return list(self.state_history)[-limit:]
    
    def reset(self) -> None:
        """Reset the state machine to initial state."""
        with self.lock:
            self.current_state = StateType.IDLE
            self.previous_state = None
            self.context = StateContext()
            self.state_history.clear()


class StateMachineAnalyzer:
    """Utility class for analyzing state machine behavior and performance."""
    
    @staticmethod
    def analyze_state_distribution(state_history: List[Dict]) -> Dict[str, float]:
        """Analyze time spent in each state."""
        state_times = defaultdict(float)
        total_time = 0
        
        for i in range(len(state_history) - 1):
            current = state_history[i]
            next_state = state_history[i + 1]
            duration = next_state['timestamp'] - current['timestamp']
            state_times[current['to'].value] += duration
            total_time += duration
        
        # Convert to percentages
        if total_time > 0:
            return {state: (time_spent / total_time) * 100 
                   for state, time_spent in state_times.items()}
        return {}
    
    @staticmethod
    def find_most_common_transitions(state_history: List[Dict]) -> List[Tuple[str, str, int]]:
        """Find most common state transitions."""
        transition_counts = defaultdict(int)
        
        for i in range(len(state_history) - 1):
            current = state_history[i]
            next_state = state_history[i + 1]
            transition = f"{current['to'].value} -> {next_state['to'].value}"
            transition_counts[transition] += 1
        
        return sorted(transition_counts.items(), key=lambda x: x[1], reverse=True)
    
    @staticmethod
    def detect_infinite_loops(state_history: List[Dict], window_size: int = 10) -> List[List[str]]:
        """Detect potential infinite loops in state transitions."""
        loops = []
        
        for i in range(len(state_history) - window_size):
            window = state_history[i:i + window_size]
            states = [entry['to'].value for entry in window]
            
            # Check for repeated patterns
            if len(set(states)) < len(states) / 2:  # More than half are duplicates
                loops.append(states)
        
        return loops


if __name__ == "__main__":
    # Demo the state machine
    sm = DialogueStateMachine()
    
    print("Initial state:", sm.get_state_info()['current_state'])
    
    # Simulate a conversation flow
    events = [
        (EventType.WAKE_WORD_DETECTED, {"user_input": "Hey Jarvis"}),
        (EventType.SPEECH_RECOGNIZED, {"recognized_text": "What time is it?"}),
        (EventType.INTENT_CLASSIFIED, {"intent": "time_query", "confidence": 0.9}),
        (EventType.RESPONSE_READY, {"response": "It's 3:30 PM"}),
    ]
    
    for event, data in events:
        print(f"\nProcessing event: {event.value}")
        sm.process_event(event, data)
        print(f"Current state: {sm.get_state_info()['current_state']}")
    
    # Analyze state machine behavior
    analyzer = StateMachineAnalyzer()
    history = sm.get_state_history()
    print(f"\nState distribution: {analyzer.analyze_state_distribution(history)}")
    print(f"Common transitions: {analyzer.find_most_common_transitions(history)}")


