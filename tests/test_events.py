"""Tests for the event system."""

import pytest

from reterm.events import EventEmitter, EventBus


def test_event_emitter_on_emit():
    """Test registering and emitting events."""
    emitter = EventEmitter()
    
    # Track event calls
    called = []
    
    # Register event handler
    def handler(sender, value=None):
        called.append(value)
    
    emitter.on("test", handler)
    
    # Emit event
    emitter.emit("test", value="hello")
    
    assert called == ["hello"]
    
    # Emit again
    emitter.emit("test", value="world")
    
    assert called == ["hello", "world"]


def test_event_emitter_off():
    """Test removing event handlers."""
    emitter = EventEmitter()
    
    # Track event calls
    called = []
    
    # Register event handlers
    def handler1(sender, value=None):
        called.append(f"handler1: {value}")
    
    def handler2(sender, value=None):
        called.append(f"handler2: {value}")
    
    emitter.on("test", handler1)
    emitter.on("test", handler2)
    
    # Emit event
    emitter.emit("test", value="hello")
    
    # Order of handlers is not guaranteed
    assert sorted(called) == sorted(["handler1: hello", "handler2: hello"])
    
    # Remove one handler
    emitter.off("test", handler1)
    called.clear()
    
    # Emit again
    emitter.emit("test", value="world")
    
    assert called == ["handler2: world"]
    
    # Remove all handlers
    emitter.off("test")
    called.clear()
    
    # Emit again
    emitter.emit("test", value="!")
    
    assert called == []


def test_event_emitter_once():
    """Test one-time event handlers."""
    emitter = EventEmitter()
    
    # Track event calls
    called = []
    
    # Register one-time event handler
    def handler(sender, value=None):
        called.append(value)
    
    emitter.once("test", handler)
    
    # Emit event
    emitter.emit("test", value="hello")
    
    assert called == ["hello"]
    
    # Emit again
    emitter.emit("test", value="world")
    
    # Handler should not be called again
    assert called == ["hello"]


def test_event_bus_singleton():
    """Test that EventBus is a singleton."""
    bus1 = EventBus()
    bus2 = EventBus()
    
    assert bus1 is bus2


def test_event_bus_events():
    """Test EventBus event handling."""
    bus = EventBus()
    
    # Track event calls
    called = []
    
    # Register event handler
    def handler(sender, value=None):
        called.append(value)
    
    bus.on("test", handler)
    
    # Emit event
    bus.emit("test", value="hello")
    
    assert called == ["hello"]
    
    # Create a new bus instance (should be the same singleton)
    bus2 = EventBus()
    
    # Emit from the new instance
    bus2.emit("test", value="world")
    
    # Handler should still be called
    assert called == ["hello", "world"]