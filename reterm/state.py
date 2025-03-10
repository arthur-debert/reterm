"""State management for the reterm framework."""

from typing import Any, Callable, Dict, List, Optional, Set, Union

from reterm.events import EventEmitter
from reterm.constants import Events


class State(EventEmitter):
    """Basic state container with change notifications."""

    def __init__(self, initial_state: Optional[Dict[str, Any]] = None):
        """Initialize the state container.
        
        Args:
            initial_state: Initial state values.
        """
        super().__init__()
        self._state = initial_state or {}
        self._previous_state = {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get a state value.
        
        Args:
            key: The state key to retrieve.
            default: Default value if the key doesn't exist.
            
        Returns:
            The state value or default.
        """
        return self._state.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a state value and emit change event.
        
        Args:
            key: The state key to set.
            value: The value to set.
        """
        old_value = self._state.get(key)
        if old_value != value:
            self._previous_state[key] = old_value
            self._state[key] = value
            self.emit(Events.STATE_CHANGE, key=key, value=value, old_value=old_value)

    def update(self, updates: Dict[str, Any]) -> None:
        """Update multiple state values at once.
        
        Args:
            updates: Dictionary of state updates.
        """
        changed_keys = []
        
        for key, value in updates.items():
            old_value = self._state.get(key)
            if old_value != value:
                self._previous_state[key] = old_value
                self._state[key] = value
                changed_keys.append(key)
        
        if changed_keys:
            self.emit(Events.STATE_CHANGE, keys=changed_keys, updates=updates)

    def get_all(self) -> Dict[str, Any]:
        """Get the entire state dictionary.
        
        Returns:
            A copy of the current state.
        """
        return self._state.copy()

    def get_previous(self, key: str, default: Any = None) -> Any:
        """Get a previous state value.
        
        Args:
            key: The state key to retrieve.
            default: Default value if the key doesn't exist.
            
        Returns:
            The previous state value or default.
        """
        return self._previous_state.get(key, default)


class StateManager:
    """Application-wide state manager."""
    
    _instance = None
    
    def __new__(cls):
        """Create a singleton instance of the state manager."""
        if cls._instance is None:
            cls._instance = super(StateManager, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the state manager."""
        if not hasattr(self, "__initialized") or not self.__initialized:
            self._states: Dict[str, State] = {}
            self.__initialized = True
    
    def create_state(self, name: str, initial_state: Optional[Dict[str, Any]] = None) -> State:
        """Create a named state container.
        
        Args:
            name: The name of the state container.
            initial_state: Initial state values.
            
        Returns:
            The created state container.
        """
        if name in self._states:
            raise ValueError(f"State '{name}' already exists")
        
        state = State(initial_state)
        self._states[name] = state
        return state
    
    def get_state(self, name: str) -> State:
        """Get a named state container.
        
        Args:
            name: The name of the state container.
            
        Returns:
            The state container.
            
        Raises:
            KeyError: If the state container doesn't exist.
        """
        if name not in self._states:
            raise KeyError(f"State '{name}' does not exist")
        
        return self._states[name]