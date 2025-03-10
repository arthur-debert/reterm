"""Event handling and propagation for the reterm framework."""

from typing import Any, Callable, Dict, List, Optional, Set, Union

from blinker import signal

from reterm.constants import Events


class EventEmitter:
    """Base class for objects that can emit events."""

    def __init__(self):
        """Initialize the event emitter."""
        self._event_handlers: Dict[str, List[Callable]] = {}
        self._signals = {}

    def on(self, event_name: str, handler: Callable) -> Callable:
        """Register an event handler.
        
        Args:
            event_name: The name of the event to listen for.
            handler: The function to call when the event is emitted.
            
        Returns:
            The handler function, to allow for method chaining.
        """
        if event_name not in self._signals:
            self._signals[event_name] = signal(event_name)
        
        self._signals[event_name].connect(handler)
        
        if event_name not in self._event_handlers:
            self._event_handlers[event_name] = []
        
        self._event_handlers[event_name].append(handler)
        return handler

    def off(self, event_name: str, handler: Optional[Callable] = None) -> None:
        """Remove an event handler.
        
        Args:
            event_name: The name of the event to stop listening for.
            handler: The handler to remove. If None, all handlers for the event are removed.
        """
        if event_name not in self._signals:
            return
        
        if handler is None:
            # Remove all handlers for this event
            if event_name in self._event_handlers:
                for h in self._event_handlers[event_name]:
                    self._signals[event_name].disconnect(h)
                self._event_handlers[event_name] = []
        else:
            # Remove specific handler
            self._signals[event_name].disconnect(handler)
            if event_name in self._event_handlers:
                if handler in self._event_handlers[event_name]:
                    self._event_handlers[event_name].remove(handler)

    def emit(self, event_name: str, *args, **kwargs) -> None:
        """Emit an event.
        
        Args:
            event_name: The name of the event to emit.
            *args: Positional arguments to pass to the event handlers.
            **kwargs: Keyword arguments to pass to the event handlers.
        """
        if event_name in self._signals:
            self._signals[event_name].send(self, **kwargs)

    def once(self, event_name: str, handler: Callable) -> Callable:
        """Register an event handler that will be called only once.
        
        Args:
            event_name: The name of the event to listen for.
            handler: The function to call when the event is emitted.
            
        Returns:
            The handler function, to allow for method chaining.
        """
        def one_time_handler(*args, **kwargs):
            self.off(event_name, one_time_handler)
            return handler(*args, **kwargs)
        
        return self.on(event_name, one_time_handler)


class EventBus(EventEmitter):
    """Global event bus for application-wide events."""
    
    _instance = None
    
    def __new__(cls):
        """Create a singleton instance of the event bus."""
        if cls._instance is None:
            cls._instance = super(EventBus, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the event bus."""
        if not hasattr(self, "_initialized") or not self._initialized:
            super().__init__()
            self._initialized = True