"""Tests for the state management system."""

import pytest

from reterm.state import State, StateManager
from reterm.constants import Events


def test_state_get_set():
    """Test getting and setting state values."""
    state = State()
    
    # Initial state should be empty
    assert state.get("key") is None
    assert state.get("key", "default") == "default"
    
    # Set a value
    state.set("key", "value")
    
    # Get the value
    assert state.get("key") == "value"
    
    # Set another value
    state.set("another", 123)
    
    # Get all values
    assert state.get_all() == {"key": "value", "another": 123}


def test_state_update():
    """Test updating multiple state values."""
    state = State()
    
    # Update multiple values
    state.update({"key1": "value1", "key2": "value2"})
    
    # Get values
    assert state.get("key1") == "value1"
    assert state.get("key2") == "value2"
    
    # Update again
    state.update({"key1": "new1", "key3": "value3"})
    
    # Get all values
    assert state.get_all() == {"key1": "new1", "key2": "value2", "key3": "value3"}


def test_state_previous_values():
    """Test getting previous state values."""
    state = State()
    
    # Set initial value
    state.set("key", "initial")
    
    # No previous value yet
    assert state.get_previous("key") is None
    
    # Update value
    state.set("key", "updated")
    
    # Previous value should be available
    assert state.get_previous("key") == "initial"
    
    # Update again
    state.set("key", "final")
    
    # Previous value should be updated
    assert state.get_previous("key") == "updated"


def test_state_change_events():
    """Test state change events."""
    state = State()
    
    # Track event calls
    events = []
    
    # Register event handler
    def handler(sender, **kwargs):
        events.append(kwargs)
    
    state.on(Events.STATE_CHANGE, handler)
    
    # Set a value
    state.set("key", "value")
    
    # Event should be emitted
    assert len(events) == 1
    assert events[0]["key"] == "key"
    assert events[0]["value"] == "value"
    assert events[0]["old_value"] is None
    
    # Update value
    state.set("key", "new_value")
    
    # Another event should be emitted
    assert len(events) == 2
    assert events[1]["key"] == "key"
    assert events[1]["value"] == "new_value"
    assert events[1]["old_value"] == "value"
    
    # Update multiple values
    state.update({"key": "final", "another": 123})
    
    # Another event should be emitted
    assert len(events) == 3
    assert "keys" in events[2]
    assert "updates" in events[2]
    assert "key" in events[2]["keys"]
    assert events[2]["updates"]["key"] == "final"
    assert events[2]["updates"]["another"] == 123


def test_state_manager_singleton():
    """Test that StateManager is a singleton."""
    manager1 = StateManager()
    manager2 = StateManager()
    
    assert manager1 is manager2


def test_state_manager_create_get_state():
    """Test creating and getting named states."""
    manager = StateManager()
    
    # Create a state
    state1 = manager.create_state("state1", {"initial": "value"})
    
    # Get the state
    state2 = manager.get_state("state1")
    
    # Should be the same state
    assert state1 is state2
    assert state1.get("initial") == "value"
    
    # Create another state
    state3 = manager.create_state("state2")
    
    # Should be a different state
    assert state1 is not state3
    
    # Try to create a state with an existing name
    with pytest.raises(ValueError):
        manager.create_state("state1")
    
    # Try to get a non-existent state
    with pytest.raises(KeyError):
        manager.get_state("non_existent")